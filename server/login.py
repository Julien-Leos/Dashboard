import secrets

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

login_page = Blueprint('login_page', __name__)


@login_page.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        body = request.form
        users = app.getDict(database.child('users'))

        if not body["email"] or not body["password"]:
            return jsonify({"message": "Error: One of the credentials is empty"}), status.HTTP_400_BAD_REQUEST
        for userName, user in users.items():
            if user["email"] == body["email"] and user["password"] == body["password"]:
                accessToken = secrets.token_hex(16)
                database.child('users').child(userName).update(
                    {"accessToken": accessToken})
                return jsonify({"message": "User successfully connected", "data": {"accessToken": accessToken}}), status.HTTP_200_OK
        return jsonify({"message": "One of the credentials is invalid."}), status.HTTP_400_BAD_REQUEST


@login_page.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        body = request.form
        users = app.getDict(database.child('users'))

        if not body["email"] or not body["password"]:
            return jsonify({"message": "Error: One of the credentials is empty"}), status.HTTP_400_BAD_REQUEST
        for user in users.values():
            if user["email"] == body["email"]:
                return jsonify({"message": "Error: A user with the same email already exist"}), status.HTTP_400_BAD_REQUEST

        accessToken = secrets.token_hex(16)
        database.child('users').push(
            {"email": body["email"], "password": body["password"], "accessToken": accessToken, "isAdmin": False, "services": ""})
        return jsonify({"message": "User successfully created", "data": {"accessToken": accessToken}}), status.HTTP_200_OK
