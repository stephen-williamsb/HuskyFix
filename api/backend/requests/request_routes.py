# api/backend/requests/requests_routes.py
from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db
from datetime import datetime

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

# Helper: convert cursor rows to list of dicts (works for cursor.fetchall())
def rows_to_dicts(cursor, rows):
    col_names = [col[0] for col in cursor.description]
    return [dict(zip(col_names, row)) for row in rows]

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
        where_clauses.append("r.studentID = %s")
        params.append(student_id)

    employee_id = request.args.get('employee_id')
    if employee_id:
        where_clauses.append("r.assignedEmployeeID = %s")
        params.append(employee_id)

    status = request.args.get('status')
    if status:
        where_clauses.append("r.status = %s")
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

    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))

    cursor = db.get_db().cursor()
    query = f"""
        SELECT
            r.requestID, r.issueType, r.description, r.status, r.priority,
            r.dateRequested, r.dateCompleted, r.buildingID, r.aptNumber,
            r.studentID, r.assignedEmployeeID
        FROM maintenanceRequest r
        {where_sql}
        ORDER BY r.dateRequested DESC
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    return make_response(jsonify(rows), 200)


# -------------------------
# POST /requests
# Create a new maintenance request (expects JSON body)
# Required fields: issueType, description, buildingID (or other location info)
# -------------------------
@requests_bp.post('')
def create_request():
    data = request.json or {}

    issueType = data.get('issueType')
    description = data.get('description')
    buildingID = data.get('buildingID')
    aptNumber = data.get('aptNumber')
    priority = data.get('priority', 'normal')
    studentID = data.get('studentID')  # optional
    dateRequested = data.get('dateRequested') or datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    if not issueType or not description or not buildingID:
        return make_response({'error': 'issueType, description and buildingID are required'}, 400)

    cursor = db.get_db().cursor()
    cursor.execute(
        """
        INSERT INTO maintenanceRequest
            (issueType, description, buildingID, aptNumber, priority, studentID, dateRequested, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (issueType, description, buildingID, aptNumber, priority, studentID, dateRequested, 'open')
    )
    db.get_db().commit()
    new_id = cursor.lastrowid
    return make_response({'requestID': new_id}, 201)


# -------------------------
# GET /requests/<id>
# Return full details for a request (photos, notes, history, status, schedule/eta, completion, assigned employees, parts)
# -------------------------
@requests_bp.get('/<int:request_id>')
def get_request_detail(request_id):
    conn = db.get_db()
    cursor = conn.cursor(dictionary=True)

    # primary request row
    cursor.execute(
        """
        SELECT r.*, b.address AS buildingAddress
        FROM maintenanceRequest r
        LEFT JOIN building b ON r.buildingID = b.buildingID
        WHERE r.requestID = %s
        """,
        (request_id,)
    )
    request_row = cursor.fetchone()
    if not request_row:
        return make_response({'error': 'Request not found'}, 404)

    # photos
    cursor.execute(
        "SELECT photoID, filePath, uploadedAt FROM requestPhotos WHERE requestID = %s ORDER BY uploadedAt DESC",
        (request_id,)
    )
    photos = rows_to_dicts(cursor, cursor.fetchall())

    # notes / comments
    cursor.execute(
        "SELECT noteID, authorID, text, createdAt FROM requestNotes WHERE requestID = %s ORDER BY createdAt DESC",
        (request_id,)
    )
    notes = rows_to_dicts(cursor, cursor.fetchall())

    # history / status timeline
    cursor.execute(
        "SELECT historyID, oldStatus, newStatus, changedBy, changedAt, note FROM requestHistory WHERE requestID = %s ORDER BY changedAt DESC",
        (request_id,)
    )
    history = rows_to_dicts(cursor, cursor.fetchall())

    # assigned employees (could be one or many depending on schema)
    cursor.execute(
        """
        SELECT e.employeeID, e.firstName, e.lastName, e.role
        FROM employee e
        JOIN requestAssignment ra ON e.employeeID = ra.employeeID
        WHERE ra.requestID = %s
        """,
        (request_id,)
    )
    assigned = rows_to_dicts(cursor, cursor.fetchall())

    # parts used / planned
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

    detail = dict(request_row)
    detail['photos'] = photos
    detail['notes'] = notes
    detail['history'] = history
    detail['assignedEmployees'] = assigned
    detail['parts'] = parts

    return make_response(jsonify(detail), 200)


# -------------------------
# PUT /requests/<id>
# Update request fields (description, location, priority, apartment, etc.)
# -------------------------
@requests_bp.put('/<int:request_id>')
def update_request(request_id):
    data = request.json or {}

    allowed = ['issueType', 'description', 'buildingID', 'aptNumber', 'priority', 'status', 'assignedEmployeeID', 'dateCompleted']
    fields = []
    values = []

    for key in allowed:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])

    if not fields:
        return make_response({'error': 'No updatable fields supplied'}, 400)

    values.append(request_id)
    cursor = db.get_db().cursor()
    cursor.execute(
        f"UPDATE maintenanceRequest SET {', '.join(fields)} WHERE requestID = %s",
        tuple(values)
    )
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

    cursor = db.get_db().cursor()
    # using status 'canceled' and recording to history table if present
    cursor.execute("UPDATE maintenanceRequest SET status = %s WHERE requestID = %s", ('canceled', request_id))
    # insert into history table if exists
    try:
        cursor.execute(
            "INSERT INTO requestHistory (requestID, oldStatus, newStatus, changedBy, changedAt, note) VALUES (%s, %s, %s, %s, NOW(), %s)",
            (request_id, 'any', 'canceled', data.get('user_id'), reason)
        )
    except Exception:
        # non-fatal if history table doesn't exist or columns differ
        pass

    db.get_db().commit()
    return make_response({'message': 'Request canceled'}, 200)
