import requests
import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

twitch_page = Blueprint('twitch_page', __name__)


@twitch_page.route('/twitch/accessToken', methods=["POST"])
def accessToken():
    if request.method == "POST":
        params = request.form
        accessToken = ""

        return jsonify(accessToken), status.HTTP_200_OK
