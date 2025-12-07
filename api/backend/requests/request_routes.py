# api/backend/requests/requests_routes.py
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime
import pymysql

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

def rows_to_dicts(cursor, rows):
    if not rows:
        return []

    # if rows are already dict-like (sqlite3.Row or true dicts)
    first = rows[0]
    if isinstance(first, dict):
        return list(rows)

    # some drivers return sqlite3.Row which acts like both tuple & dict
    try:
        return [dict(row) for row in rows]
    except Exception:
        pass

    # fallback to tuple + description conversion
    col_names = [col[0] for col in cursor.description]
    return [dict(zip(col_names, row)) for row in rows]


def row_to_dict(cursor, row):
    if row is None:
        return None

    if isinstance(row, dict):
        return row

    try:
        return dict(row)
    except Exception:
        pass

    col_names = [col[0] for col in cursor.description]
    return dict(zip(col_names, row))


# -------------------------
# GET /requests
# Return list of requests, filterable by student, employee, status, date range, priority
# Query params supported:
#   student_id, employee_id, status, start_date, end_date, priority, limit, offset
# -------------------------
@requests_bp.get('')
def list_requests():
    params = []
    where_clauses = []

    student_id = request.args.get('student_id')
    if student_id:
        # schema uses studentRequestingID
        where_clauses.append("r.studentRequestingID = %s")
        params.append(student_id)

    employee_id = request.args.get('employee_id')
    if employee_id:
        # employeeAssigned is a join table: filter by existence
        where_clauses.append(
            "EXISTS (SELECT 1 FROM employeeAssigned ea WHERE ea.requestID = r.requestID AND ea.employeeID = %s)"
        )
        params.append(employee_id)

    status = request.args.get('status')
    if status:
        # schema uses activeStatus
        where_clauses.append("r.activeStatus = %s")
        params.append(status)

    priority = request.args.get('priority')
    if priority:
        where_clauses.append("r.priority = %s")
        params.append(priority)

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        where_clauses.append("r.dateRequested BETWEEN %s AND %s")
        params.append(start_date)
        params.append(end_date)
    elif start_date:
        where_clauses.append("r.dateRequested >= %s")
        params.append(start_date)
    elif end_date:
        where_clauses.append("r.dateRequested <= %s")
        params.append(end_date)

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    try:
        limit = int(request.args.get('limit', 100))
    except ValueError:
        limit = 100
    try:
        offset = int(request.args.get('offset', 0))
    except ValueError:
        offset = 0

    cursor = db.get_db().cursor()
    query = f"""
        SELECT
            r.requestID,
            r.issueType,
            r.issueDescription,
            r.activeStatus,
            r.priority,
            r.dateRequested,
            r.dateCompleted,
            r.buildingID,
            r.aptNumber,
            r.studentRequestingID
        FROM maintenanceRequest r
        {where_sql}
        ORDER BY r.dateRequested DESC
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    results = rows_to_dicts(cursor, rows)
    return make_response(jsonify(results), 200)


# -------------------------
# POST /requests
# Create a new maintenance request (expects JSON body)
# Accepts external fields 'description' and 'studentID' and maps to DB columns
# -------------------------
@requests_bp.post('')
def create_request():
    data = request.json or {}

    issueType = data.get('issueType')
    description = data.get('description')
    buildingID = data.get('buildingID')
    aptNumber = data.get('aptNumber')
    priority = data.get('priority', 0)
    studentID = data.get('studentID')
    dateRequested = data.get('dateRequested') or datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # basic validation
    if not issueType or not description or not buildingID:
        return make_response({'error': 'issueType, description and buildingID are required'}, 400)

    try:
        aptNumber = int(aptNumber)
    except Exception:
        return make_response({'error': 'aptNumber must be an integer'}, 400)

    conn = db.get_db()
    cursor = conn.cursor()

    #tried to add auto increment but it broke db so we are doing this now.
    cursor.execute("SELECT COALESCE(MAX(requestID), 0) + 1 FROM maintenanceRequest")
    row = cursor.fetchone()
    new_id = list(row.values())[0]


    insert_sql = """
        INSERT INTO maintenanceRequest
            (requestID, issueType, issueDescription, buildingID, aptNumber,
             priority, studentRequestingID, dateRequested, activeStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        new_id,
        issueType,
        description,
        buildingID,
        aptNumber,
        priority,
        studentID,
        dateRequested,
        'open'
    )

    try:
        cursor.execute(insert_sql, params)
        conn.commit()
        return make_response({'requestID': new_id}, 201)

    except Exception as e:
        conn.rollback()
        current_app.logger.exception("Failed to create maintenance request")
        return make_response({'error': str(e)}, 500)


# -------------------------
# GET /requests/<id>
# Return full details for a request (photos, notes, history, status, schedule/eta, completion, assigned employees, parts)
# -------------------------
@requests_bp.get('/<int:request_id>')
def get_request_detail(request_id):
    conn = db.get_db()
    cursor = conn.cursor()

    # primary request row (use actual column names)
    cursor.execute(
        """
        SELECT r.*, b.address AS buildingAddress
        FROM maintenanceRequest r
        LEFT JOIN building b ON r.buildingID = b.buildingID
        WHERE r.requestID = %s
        """,
        (request_id,)
    )
    request_row_raw = cursor.fetchone()
    if not request_row_raw:
        return make_response({'error': 'Request not found'}, 404)
    request_row = row_to_dict(cursor, request_row_raw)

    # photos: check if a requestPhotos table exists; if not fallback to issuePhotos text field
    photos = []
    try:
        cursor.execute(
            "SELECT photoID, filePath, uploadedAt FROM requestPhotos WHERE requestID = %s ORDER BY uploadedAt DESC",
            (request_id,)
        )
        photos = rows_to_dicts(cursor, cursor.fetchall())
    except Exception:
        if 'issuePhotos' in (request_row or {}) and request_row.get('issuePhotos'):
            photos = [{'embedded': request_row.get('issuePhotos')}]

    # notes / comments (try table, else use completionNotes)
    notes = []
    try:
        cursor.execute(
            "SELECT noteID, authorID, text, createdAt FROM requestNotes WHERE requestID = %s ORDER BY createdAt DESC",
            (request_id,)
        )
        notes = rows_to_dicts(cursor, cursor.fetchall())
    except Exception:
        if 'completionNotes' in (request_row or {}) and request_row.get('completionNotes'):
            notes = [{'note': request_row.get('completionNotes')}]

    # history / status timeline (try table; otherwise empty list)
    history = []
    try:
        cursor.execute(
            "SELECT historyID, oldStatus, newStatus, changedBy, changedAt, note FROM requestHistory WHERE requestID = %s ORDER BY changedAt DESC",
            (request_id,)
        )
        history = rows_to_dicts(cursor, cursor.fetchall())
    except Exception:
        history = []

    # assigned employees (pull from employeeAssigned join table)
    try:
        cursor.execute(
            """
            SELECT e.employeeID, e.firstName, e.lastName, e.employeeType
            FROM employee e
            JOIN employeeAssigned ea ON e.employeeID = ea.employeeID
            WHERE ea.requestID = %s
            """,
            (request_id,)
        )
        assigned = rows_to_dicts(cursor, cursor.fetchall())
    except Exception:
        assigned = []

    # parts used / planned
    parts = []
    try:
        cursor.execute(
            """
            SELECT p.partID, p.name, pu.quantity, p.cost
            FROM partUsed pu
            JOIN part p ON pu.partID = p.partID
            WHERE pu.requestID = %s
            """,
            (request_id,)
        )
        parts = rows_to_dicts(cursor, cursor.fetchall())
    except Exception:
        parts = []

    # combine into response
    detail = dict(request_row) if request_row else {}
    detail['photos'] = photos
    detail['notes'] = notes
    detail['history'] = history
    detail['assignedEmployees'] = assigned
    detail['parts'] = parts

    return make_response(jsonify(detail), 200)


# -------------------------
# PUT /requests/<id>
# Update request fields (maps external keys to DB column names; supports assigning employee)
# -------------------------
@requests_bp.put('/<int:request_id>')
def update_request(request_id):
    data = request.json or {}

    # mapping of accepted external keys to DB column names
    mapping = {
        'issueType': 'issueType',
        'description': 'issueDescription',
        'buildingID': 'buildingID',
        'aptNumber': 'aptNumber',
        'priority': 'priority',
        'status': 'activeStatus',        # external 'status' -> DB 'activeStatus'
        'dateCompleted': 'dateCompleted',
        'scheduledDate': 'scheduledDate',
        'issuePhotos': 'issuePhotos',
        'completionNotes': 'completionNotes'
    }

    fields = []
    values = []
    for ext_key, db_col in mapping.items():
        if ext_key in data:
            fields.append(f"{db_col} = %s")
            values.append(data[ext_key])

    if not fields and 'assignedEmployeeID' not in data:
        return make_response({'error': 'No updatable fields supplied'}, 400)

    cursor = db.get_db().cursor()
    if fields:
        values.append(request_id)
        cursor.execute(
            f"UPDATE maintenanceRequest SET {', '.join(fields)} WHERE requestID = %s",
            tuple(values)
        )

    # handle assignedEmployeeID separately using employeeAssigned join table
    if 'assignedEmployeeID' in data:
        emp_id = data.get('assignedEmployeeID')
        try:
            # optionally remove duplicates then insert
            cursor.execute("DELETE FROM employeeAssigned WHERE requestID = %s AND employeeID = %s", (request_id, emp_id))
            cursor.execute("INSERT INTO employeeAssigned (employeeID, requestID) VALUES (%s, %s)", (emp_id, request_id))
        except Exception:
            # If schema differs, ignore but log
            current_app.logger.exception("Could not update employeeAssigned for request %s", request_id)

    db.get_db().commit()
    return make_response({'message': 'Request updated'}, 200)


# -------------------------
# DELETE /requests/<id>
# Soft-delete / cancel a request (mark canceled or archived)
# -------------------------
@requests_bp.delete('/<int:request_id>')
def cancel_request(request_id):
    data = request.json or {}
    reason = data.get('reason', 'Canceled via API')
    user_id = data.get('user_id')

    cursor = db.get_db().cursor()
    # set activeStatus to 'canceled' (matches schema)
    cursor.execute("UPDATE maintenanceRequest SET activeStatus = %s WHERE requestID = %s", ('canceled', request_id))

    # try to add a row to requestHistory if table exists
    try:
        cursor.execute(
            "INSERT INTO requestHistory (requestID, oldStatus, newStatus, changedBy, changedAt, note) VALUES (%s, %s, %s, %s, NOW(), %s)",
            (request_id, 'any', 'canceled', user_id, reason)
        )
    except Exception:
        # non-fatal if history table doesn't exist or columns differ
        current_app.logger.debug("requestHistory insert failed (table may be missing or schema differs)")

    db.get_db().commit()
    return make_response({'message': 'Request canceled'}, 200)