from flask import Blueprint
from flask import request
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
            return "Error: One of the credentials is empty", status.HTTP_400_BAD_REQUEST
        for user in users:
            if user[1]["email"] == data["email"]:
                return "Error: A user with the same email already exist", status.HTTP_400_BAD_REQUEST

        database.child('users').push(
            {"email": data["email"], "password": data["password"]})
        return "User successfully created", status.HTTP_200_OK


@sign_page.route('/signIn', methods=["POST"])
def signIn():
    if request.method == "POST":
        data = request.form
        users = app.getChildItems(database.child('users'))

        if not data["email"] or not data["password"]:
            return "Error: One of the credentials is empty", status.HTTP_400_BAD_REQUEST
        for user in users:
            if user[1]["email"] == data["email"] and user[1]["password"] == data["password"]:
                return "User successfully connected", status.HTTP_200_OK
        return "One of the credentials is invalid.", status.HTTP_400_BAD_REQUEST