import secrets

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

sign_page = Blueprint('sign_page', __name__)


@sign_page.route('/signUp', methods=["POST"])
def signUp():
    if request.method == "POST":
        data = request.form
        users = app.getChildItems(database.child('users'))

        if not data["email"] or not data["password"]:
            return jsonify({"message": "Error: One of the credentials is empty"}), status.HTTP_400_BAD_REQUEST
        for user in users:
            if user[1]["email"] == data["email"]:
                return jsonify({"message": "Error: A user with the same email already exist"}), status.HTTP_400_BAD_REQUEST

        database.child('users').push(
            {"email": data["email"], "password": data["password"], "access_token": "None"})
        return jsonify({"message": "User successfully created"}), status.HTTP_200_OK


@sign_page.route('/signIn', methods=["POST"])
def signIn():
    if request.method == "POST":
        data = request.form
        users = app.getChildItems(database.child('users'))

        if not data["email"] or not data["password"]:
            return jsonify({"message": "Error: One of the credentials is empty"}), status.HTTP_400_BAD_REQUEST
        for user in users:
            if user[1]["email"] == data["email"] and user[1]["password"] == data["password"]:
                access_token = secrets.token_hex(16)
                database.child('users').child(user[0]).update(
                    {"access_token": access_token})
                return jsonify({"message": "User successfully connected", "data": {"access_token": access_token}}), status.HTTP_200_OK
        return jsonify({"message": "One of the credentials is invalid."}), status.HTTP_400_BAD_REQUEST
