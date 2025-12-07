from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
report = Blueprint("report", __name__)


@report.route("/active_requests", methods=["GET"])
def get_active_requests():
    cursor = db.get_db().cursor()
    query = "SELECT * FROM maintenanceRequest WHERE activeStatus != 'completed'"
    cursor.execute(query)
    return jsonify(cursor.fetchall()), 200


@report.route("/AVG_Monthly_Requests", methods=["GET"])
def get_monthly_requests():
    cursor = db.get_db().cursor()
    params = []
    from_date = request.args.get("from")
    until_date = request.args.get("to")
    query = (
        "SELECT m.issueType, COUNT(*) / TIMESTAMPDIFF(MONTH, %s, %s) AS `AVG requests per month` "
        "FROM maintenanceRequest m WHERE m.dateRequested BETWEEN %s AND %s")
    params.extend([from_date, until_date, from_date, until_date])
    request_type = request.args.get("type")
    if request_type:
        query += " AND m.issueType = %s"
        params.append(request_type)

    query += " GROUP BY (m.issueType) ORDER BY `AVG requests per month`"
    sort_desc = request.args.get("desc").lower() == "true"
    if sort_desc:
        query += " DESC"
    cursor.execute(query, params)
    return jsonify(cursor.fetchall()), 200


@report.route("/building_requests", methods=["GET"])
def get_building_requests():
    cursor = db.get_db().cursor()
    params = []
    from_date = request.args.get("from")
    until_date = request.args.get("to")
    query = ("SELECT b.address, COUNT(*) AS totalRequests "
             "FROM maintenanceRequest m "
             "JOIN building b ON m.buildingID = b.buildingID "
             "WHERE m.dateRequested BETWEEN %s AND %s")
    params.extend([from_date, until_date])
    building = request.args.get("building")
    if building:
        query += " AND b.address = %s"
        params.append(building)
    only_active = request.args.get("active").lower() == "true"
    if only_active:
        query += " AND m.activeStatus != 'Completed'"
    query += "GROUP BY b.buildingID, b.address ORDER BY totalRequests"
    sort_desc = request.args.get("desc").lower() == "true"
    if sort_desc:
        query += " DESC"
    cursor.execute(query, params)
    return jsonify(cursor.fetchall()), 200


@report.route("/revenue", methods=["GET"])
def get_revenue():
    cursor = db.get_db().cursor()
    by_build = request.args.get("by_build").lower() == "true"
    query = ""
    params = []
    if by_build:
        query += "SELECT b.address, SUM(%s * a.rentalCost) AS totalRevenue"
    else:
        query += "SELECT SUM(%s * a.rentalCost) AS totalRevenue"
    interval = request.args.get("interval")
    if interval == "Year":
        params.append(12)
    else:
        params.append(1)
    query += " FROM apartment a JOIN building b on a.buildingID = b.buildingID"
    include_empty = request.args.get("include_empty").lower() == "true"
    if not include_empty:
        query += " WHERE a.renterID IS NOT NULL"
    if by_build:
        query += " GROUP BY b.buildingID, b.address ORDER BY totalRevenue DESC"
    cursor.execute(query, params)
    return jsonify(cursor.fetchall()), 200


@report.route("/cost", methods=["GET"])
def get_cost():
    cursor = db.get_db().cursor()
    by_build = request.args.get("by_build").lower() == "true"
    query = ""
    params = []
    if by_build:
        query += "SELECT b.address, SUM(p.cost) AS totalCost"
    else:
        query += "SELECT SUM(p.cost) AS totalCost"

    query += (" FROM maintenanceRequest m JOIN partUsed pu ON m.requestID = pu.requestID "
              "JOIN part p ON pu.partID = p.partID JOIN building b ON b.buildingID = m.buildingID "
              "WHERE m.dateCompleted BETWEEN %s AND %s")
    from_date = request.args.get("from")
    until_date = request.args.get("to")
    params.extend([from_date, until_date])
    if by_build:
        query += " GROUP BY b.buildingID, b.address ORDER BY totalCost DESC"

    cursor.execute(query, params)
    return jsonify(cursor.fetchall()), 200


@report.route("/vacancies", methods=["GET"])
def get_vacancies():
    cursor = db.get_db().cursor()
    by_build = request.args.get("by_build").lower() == "true"
    query = ""
    if by_build:
        query += "SELECT b.address, COUNT(*) AS vacancies"
    else:
        query += "SELECT COUNT(*) AS `Total vacancies`"
    query +=  (" FROM building b "
               "JOIN apartment a ON a.buildingID = b.buildingID "
               "WHERE a.renterID IS NULL")
    if by_build:
        query += " GROUP BY b.buildingId, b.address ORDER BY vacancies DESC"
    cursor.execute(query)
    return jsonify(cursor.fetchall()), 200
