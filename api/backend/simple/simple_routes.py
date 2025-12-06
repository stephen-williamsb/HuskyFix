from crypt import methods

from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)
import json
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import model01

# This blueprint handles some basic routes that you can use for testing
simple_routes = Blueprint("simple_routes", __name__)


# ------------------------------------------------------------
# / is the most basic route
# Once the api container is started, in a browser, go to
# localhost:4000/playlist
@simple_routes.route("/")
def welcome():
    current_app.logger.info("GET / handler")
    welcome_message = "<h1>Welcome to the CS 3200 Project Template REST API"
    response = make_response(welcome_message)
    response.status_code = 200
    return response


# ------------------------------------------------------------
# /playlist returns the sample playlist data contained in playlist.py
# (imported above)
@simple_routes.route("/playlist")
def get_playlist_data():
    current_app.logger.info("GET /playlist handler")
    response = make_response(jsonify(sample_playlist_data))
    response.status_code = 200
    return response


# ------------------------------------------------------------
@simple_routes.route("/niceMessage", methods=["GET"])
def affirmation():
    current_app.logger.info("GET /niceMessage")
    message = """
    <H1>Think about it...</H1>
    <br />
    You only need to be 1% better today than you were yesterday!
    """
    response = make_response(message)
    response.status_code = 200
    return response


# ------------------------------------------------------------
# Demonstrates how to redirect from one route to another.
@simple_routes.route("/message")
def mesage():
    return redirect(url_for(affirmation))


@simple_routes.route("/data")
def getData():
    current_app.logger.info("GET /data handler")

    # Create a simple dictionary with nested data
    data = {"a": {"b": "123", "c": "Help"}, "z": {"b": "456", "c": "me"}}

    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@simple_routes.route("/prediction/<var_01>/<var_02>", methods=["GET"])
def get_prediction(var_01, var_02):
    current_app.logger.info("GET /prediction handler")

    try:
        # Call prediction function from model01
        prediction = model01.predict(var_01, var_02)
        current_app.logger.info(f"prediction value returned is {prediction}")

        response_data = {
            "prediction": prediction,
            "input_variables": {"var01": var_01, "var02": var_02},
        }

        response = make_response(jsonify(response_data))
        response.status_code = 200
        return response

    except Exception as e:
        response = make_response(
            jsonify({"error": "Error processing prediction request"})
        )
        response.status_code = 500
        return response


@simple_routes.route("/report/active_requests", methods=["GET"])
def get_active_requests():
    cursor = db.get_db().cursor()
    query = "SELECT * FROM maintenanceRequest WHERE activeStatus != 'completed'"
    cursor.execute(query)
    return jsonify(cursor.fetchall()), 200


@simple_routes.route("/report/AVG_Monthly_Requests", methods=["GET"])
def get_monthly_requests():
    cursor = db.get_db().cursor()
    query = (
        "SELECT m.issueType, COUNT(*) / TIMESTAMPDIFF(MONTH, '2025-01-01', '2025-11-23') AS `AVG requests per month` "
        "FROM maintenanceRequest m WHERE m.dateRequested BETWEEN '2025-01-01' AND '2025-11-23' "
        "GROUP BY (m.issueType) ORDER BY `AVG requests per month`;")
    cursor.execute(query)
    return cursor.fetchone()


@simple_routes.route("/report/building_requests", methods=["GET"])
def get_building_requests():
    cursor = db.get_db().cursor()
    query = ("SELECT b.address, COUNT(*) AS totalRequests "
             "FROM maintenanceRequest m "
             "JOIN building b ON m.buildingID = b.buildingID "
             "GROUP BY b.buildingID, b.address "
             "ORDER BY totalRequests;")
    cursor.execute(query)
    return cursor.fetchone()


@simple_routes.route("/report/revenue", methods=["GET"])
def get_revenue():
    cursor = db.get_db().cursor()
    query = ("SELECT SUM(a.rentalCost) AS totalRevenue "
             "FROM apartment a"
             "WHERE renterId IS NOT NULL;")
    cursor.execute(query)
    return cursor.fetchone()


@simple_routes.route("/report/cost", methods=["GET"])
def get_cost():
    cursor = db.get_db().cursor()
    query = ("SELECT SUM(p.cost) AS totalCost "
             "FROM maintenanceRequest m"
             "JOIN peartUsed pu ON m.requestID = pu.requestID"
             "JOIN part p ON pu.partID = p.partID;")
    cursor.execute(query)
    return cursor.fetchone()


@simple_routes.route("/report/vacancies", methods=["GET"])
def get_vacancies():
    cursor = db.get_db().cursor()
    query = ("SELECT b.address, COUNT(*) AS vacancies "
             "FROM building b "
             "JOIN apartment a ON b.buildingID = a.buildingID "
             "WHERE a.renterId IS NULL"
             "GROUP BY b.buildingID, b.address "
             "ORDER BY vacancies;")
    cursor.execute(query)
    return cursor.fetchone()

