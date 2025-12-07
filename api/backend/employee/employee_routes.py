from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

# Helper to convert rows to list[dict]
def rows_to_dicts(cursor, rows):
    col_names = [col[0] for col in cursor.description]
    return [dict(zip(col_names, row)) for row in rows]

# /employee/parts

# GET: list parts inventory (quantities, cost)
@employee_bp.get('/parts')
def get_parts_inventory():
    
    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT partID, name, cost, quantity
        FROM part
        ORDER BY name
        """
    )
    rows = cursor.fetchall()

    return make_response(jsonify(rows), 200)

# POST: add new part to inventory
@employee_bp.post('/parts')
def add_part():
    data = request.json or {}

    name = data.get('name')
    cost = data.get('cost')
    quantity = data.get('quantity', 0)

    if not name or cost is None:
        return make_response({'error': 'name and cost are required'}, 400)

    cursor = db.get_db().cursor()
    cursor.execute(
        """
        INSERT INTO part (name, cost, quantity)
        VALUES (%s, %s, %s)
        """,
        (name, cost, quantity)
    )
    db.get_db().commit()

    new_id = cursor.lastrowid
    return make_response({'partID': new_id}, 201)

# PUT: update part quantity / price / metadata
@employee_bp.put('/parts/<int:part_id>')
def update_part(part_id):
    data = request.json or {}

    fields = []
    values = []

    if 'name' in data:
        fields.append('name = %s')
        values.append(data['name'])

    if 'cost' in data:
        fields.append('cost = %s')
        values.append(data['cost'])

    if 'quantity' in data:
        fields.append('quantity = %s')
        values.append(data['quantity'])

    if not fields:
        return make_response({'error': 'No updatable fields supplied'}, 400)

    values.append(part_id)

    cursor = db.get_db().cursor()
    cursor.execute(
        f"""
        UPDATE part
        SET {', '.join(fields)}
        WHERE partID = %s
        """,
        tuple(values)
    )
    db.get_db().commit()

    return make_response({'message': 'Part updated'}, 200)

# /employee/parts/{id}

# GET: part detail including usage history
@employee_bp.get('/parts/<int:part_id>')
def get_part_detail(part_id):
    cursor = db.get_db().cursor(dictionary=True)

    cursor.execute(
        """
        SELECT partID, name, cost, quantity
        FROM part
        WHERE partID = %s
        """,
        (part_id,)
    )
    row = cursor.fetchone()
    if not row:
        return make_response({'error': 'Part not found'}, 404)

    col_names = [col[0] for col in cursor.description]
    part = dict(zip(col_names, row))

    cursor.execute(
        """
        SELECT
            pu.requestID,
            mr.issueType,
            mr.dateRequested,
            mr.dateCompleted,
            b.address AS buildingAddress,
            mr.aptNumber
        FROM partUsed pu
        JOIN maintenanceRequest mr ON pu.requestID = mr.requestID
        JOIN building b ON mr.buildingID = b.buildingID
        WHERE pu.partID = %s
        ORDER BY mr.dateRequested DESC
        """,
        (part_id,)
    )
    usage_rows = cursor.fetchall()
    part['usage'] = rows_to_dicts(cursor, usage_rows)

    return make_response(jsonify(part), 200)

# PUT: adjust quantity or mark defective/returned
@employee_bp.put('/parts/<int:part_id>/status')
def adjust_part_status(part_id):
    data = request.json or {}
    quantity_delta = data.get('quantity_delta')

    if quantity_delta is None:
        return make_response({'error': 'quantity_delta is required'}, 400)

    cursor = db.get_db().cursor()
    cursor.execute(
        """
        UPDATE part
        SET quantity = quantity + %s
        WHERE partID = %s
        """,
        (quantity_delta, part_id)
    )
    db.get_db().commit()

    return make_response({'message': 'Part quantity adjusted'}, 200)

# /employee/reports/monthly-cost

# GET: monthly maintenance cost report
@employee_bp.get('/reports/monthly-cost')
def monthly_maintenance_cost():
    cursor = db.get_db().cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            b.buildingID,
            b.address,
            SUM(p.cost) AS totalCost
        FROM maintenanceRequest m
        JOIN building b ON m.buildingID = b.buildingID
        JOIN partUsed pu ON m.requestID = pu.requestID
        JOIN part p ON pu.partID = p.partID
        WHERE MONTH(m.dateCompleted) = MONTH(CURDATE())
          AND YEAR(m.dateCompleted) = YEAR(CURDATE())
        GROUP BY b.buildingID, b.address
        ORDER BY b.buildingID
        """
    )
    rows = cursor.fetchall()
    return make_response(jsonify(rows), 200)


# /employe/reports/revenue

# GET: total revenue in a period
@employee_bp.get('/reports/revenue')
def revenue_report():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return make_response({'error': 'start and end parameters required'}, 400)

    cursor = db.get_db().cursor(dictionary=True)
    cursor.execute(
        """
        SELECT SUM(a.rentalCost) AS totalRevenue
        FROM apartment a
        WHERE renterId IS NOT NULL
          AND a.dateRented BETWEEN %s AND %s
        """,
        (start, end)
    )
    return make_response(jsonify(cursor.fetchone()), 200)