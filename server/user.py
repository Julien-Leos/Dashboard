import secrets

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

users_page = Blueprint('users_page', __name__)


@users_page.route('/users', defaults={'name': None})
@users_page.route('/users/<name>', methods=["GET", "POST", "PUT", "DELETE"])
def users(name):
    header = request.headers
    body = request.form
    users = app.getChildItems(database.child('users'))

    if not app.checkAccessToken(header, users):
        return jsonify({"message": "User not authorized"}), status.HTTP_401_UNAUTHORIZED

    if request.method == "POST":
        body = request.form
        users = app.getChildItems(database.child('users'))

        if not body["email"] or not body["password"]:
            return jsonify({"message": "Error: One of the credentials is empty"}), status.HTTP_400_BAD_REQUEST
        for user in users:
            if user[1]["email"] == body["email"]:
                return jsonify({"message": "Error: A user with the same email already exist"}), status.HTTP_400_BAD_REQUEST

        database.child('users').push(
            {"email": body["email"], "password": body["password"], "accessToken": "None"})
        return jsonify({"message": "User successfully created"}), status.HTTP_200_OK