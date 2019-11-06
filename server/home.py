from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

home_page = Blueprint('home_page', __name__)


@home_page.route('/home', methods=["GET"])
def home():
    if request.method == "GET":
        print("----TOTO----\n")
        print(request.headers)
        print("\n----TATA----")
        header = request.headers
        users = app.getChildItems(database.child('users'))

        if not app.checkAccessToken(header, users):
            return jsonify({"message": "User not authorized"}), status.HTTP_401_UNAUTHORIZED
        return jsonify({"message": "Home data successfully get"}), status.HTTP_200_OK
