import requests
import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

twitch_page = Blueprint('twitch_page', __name__)


@twitch_page.route('/twitch/oauth2', methods=["GET"])
def oauth2():
    clientId = "apxc8zgwnv9ggecemvoesem2u484i5"
    redirectUri = "http://localhost:3000/services?from=twitch"
    scope = "user:edit"

    return jsonify("https://id.twitch.tv/oauth2/authorize?client_id=" + clientId + "&redirect_uri=" + redirectUri + "&response_type=token&scope=" + scope)
