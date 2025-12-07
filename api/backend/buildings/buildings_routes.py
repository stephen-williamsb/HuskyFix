# api/backend/building/building_routes.py

from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

building_bp = Blueprint('building', __name__, url_prefix='/buildings')


# Helper function to convert DB rows to list of dicts
def rows_to_dicts(cursor, rows):
    col_names = [col[0] for col in cursor.description]
    return [dict(zip(col_names, row)) for row in rows]

#/buildings

# 1) GET /buildings
@building_bp.get('/')
def list_buildings():

    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT
            b.buildingID,
            b.address,
            COUNT(DISTINCT a.aptNumber) AS numApartments,
            SUM(CASE WHEN a.renterId IS NULL THEN 1 ELSE 0 END) AS vacancies,
            COUNT(DISTINCT m.requestID) AS totalRequests
        FROM building b
        LEFT JOIN apartment a
            ON b.buildingID = a.buildingID
        LEFT JOIN maintenanceRequest m
            ON m.buildingID = b.buildingID
        GROUP BY b.buildingID, b.address
        ORDER BY b.buildingID
        """
    )
    rows = cursor.fetchall()
    return make_response(jsonify(rows_to_dicts(cursor, rows)), 200)


# 2) POST /buildings
@building_bp.post('/')
def create_building():
    data = request.json or {}
    address = data.get('address')
    manager_id = data.get('managerID')

    if not address or manager_id is None:
        return make_response(
            {'error': 'Need address and managerID'}, 400
        )

    cursor = db.get_db().cursor()
    cursor.execute(
        """
        INSERT INTO building (address, managerID)
        VALUES (%s, %s)
        """,
        (address, manager_id)
    )
    db.get_db().commit()
    new_id = cursor.lastrowid

    return make_response({'buildingID': new_id}, 201)


# 3) PUT /buildings/<building_id>
@building_bp.put('/<int:building_id>')
def update_building(building_id):
    data = request.json or {}
    fields = []
    values = []

    if 'address' in data:
        fields.append('address = %s')
        values.append(data['address'])

    if 'managerID' in data:
        fields.append('managerID = %s')
        values.append(data['managerID'])

    if not fields:
        return make_response({'error': 'No updatable fields.'}, 400)

    values.append(building_id)

    cursor = db.get_db().cursor()
    cursor.execute(
        f"""
        UPDATE building
        SET {', '.join(fields)}
        WHERE buildingID = %s
        """,
        tuple(values)
    )
    db.get_db().commit()

    return make_response({'message': 'building update successful'}, 200)


# 4) GET /buildings/<building_id>/apartments
@building_bp.get('/<int:building_id>/apartments')
def list_apartments(building_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT
            a.buildingID,
            a.aptNumber,
            a.rentalCost,
            a.dateRented,
            a.renterId,
            CASE WHEN a.renterId IS NULL THEN 1 ELSE 0 END AS isVacant
        FROM apartment a
        WHERE a.buildingID = %s
        ORDER BY a.aptNumber
        """,
        (building_id,)
    )
    rows = cursor.fetchall()
    return make_response(jsonify(rows_to_dicts(cursor, rows)), 200)


# 5) PUT /buildings/<building_id>/apartments/<apt_number>
@building_bp.put('/<int:building_id>/apartments/<int:apt_number>')
def update_apartment(building_id, apt_number):
    data = request.json or {}
    fields = []
    values = []

    if 'rentalCost' in data:
        fields.append('rentalCost = %s')
        values.append(data['rentalCost'])

    if 'renterId' in data:
        fields.append('renterId = %s')
        values.append(data['renterId'])

    if 'dateRented' in data:
        fields.append('dateRented = %s')
        values.append(data['dateRented'])

    if not fields:
        return make_response({'error': 'No updatable fields'}, 400)

    values.extend([building_id, apt_number])

    cursor = db.get_db().cursor()
    cursor.execute(
        f"""
        UPDATE apartment
        SET {', '.join(fields)}
        WHERE buildingID = %s AND aptNumber = %s
        """,
        tuple(values)
    )
    db.get_db().commit()

    return make_response({'message': 'apartment update successful'}, 200)


# 6) GET /buildings/<building_id>/apartments/<apt_number>/vacancy
@building_bp.get('/<int:building_id>/apartments/<int:apt_number>/vacancy')
def get_vacancy(building_id, apt_number):
    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT
            buildingID,
            aptNumber,
            renterId,
            rentalCost,
            CASE WHEN renterId IS NULL THEN 1 ELSE 0 END AS isVacant
        FROM apartment
        WHERE buildingID = %s AND aptNumber = %s
        """,
        (building_id, apt_number)
    )
    row = cursor.fetchone()
    if not row:
        return make_response({'error': 'apartment not exist'}, 404)

    return make_response(jsonify(rows_to_dicts(cursor, [row])[0]), 200)


# 7) PUT /buildings/<building_id>/apartments/<apt_number>/vacancy
@building_bp.put('/<int:building_id>/apartments/<int:apt_number>/vacancy')
def set_vacancy(building_id, apt_number):
    data = request.json or {}

    if 'renterId' not in data:
        return make_response({'error': 'Need renterId（Can be null）'}, 400)

    renter_id = data['renterId']

    cursor = db.get_db().cursor()
    if renter_id is None:
        cursor.execute(
            """
            UPDATE apartment
            SET renterId = NULL,
                dateRented = NULL
            WHERE buildingID = %s AND aptNumber = %s
            """,
            (building_id, apt_number)
        )
    else:
        cursor.execute(
            """
            UPDATE apartment
            SET renterId = %s,
                dateRented = CURDATE()
            WHERE buildingID = %s AND aptNumber = %s
            """,
            (renter_id, building_id, apt_number)
        )

    db.get_db().commit()
    return make_response({'message': 'vacancy status updated'}, 200)
