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


@twitch_page.route('/twitch/live_viewer', methods=["POST"])
def live_viewer():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": [{"value": params["streamer"]}]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/streams?user_login=" + params["streamer"], headers={"Client-ID": "apxc8zgwnv9ggecemvoesem2u484i5"}).content)
    jsonResponse["items"].append(
        {"span": 2, "value": str(twitchResponse["data"][0]["viewer_count"]) + " viewers"})
    return jsonify(jsonResponse), status.HTTP_200_OK


@twitch_page.route('/twitch/live_best', methods=["POST"])
def live_best():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": [
            {
                "span": 1,
                "value": params["game"]
            }, {
                "span": 20,
                "value": {
                    "direction": "column",
                    "items": []
                }
            }
        ]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/games?name=" + params["game"], headers={"Client-ID": "apxc8zgwnv9ggecemvoesem2u484i5"}).content)
    gameId = twitchResponse["data"][0]["id"]
    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/streams?game_id=" + gameId, headers={"Client-ID": "apxc8zgwnv9ggecemvoesem2u484i5"}).content)
    for stream in twitchResponse["data"]:
        newStream = {
            "direction": "row",
            "items": [
                {
                    "span": 2,
                    "value": stream["user_name"]
                },
                {
                    "value": stream["viewer_count"]
                }
            ]
        }
        jsonResponse["items"][1]["value"]["items"].append(
            {"value": newStream, "link": "https://www.twitch.tv/" + stream["user_name"]})
    return jsonify(jsonResponse), status.HTTP_200_OK

@twitch_page.route('/twitch/streamer_sub', methods=["POST"])
def streamer_sub():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": [{"value": params["streamer"]}]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users?login=" + params["streamer"], headers={"Client-ID": "apxc8zgwnv9ggecemvoesem2u484i5"}).content)
    streamerId = twitchResponse["data"][0]["id"]
    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users/follows?to_id=" + streamerId, headers={"Client-ID": "apxc8zgwnv9ggecemvoesem2u484i5"}).content)
    jsonResponse["items"].append(
        {"span": 2, "value": str(twitchResponse["total"]) + " subs"})
    return jsonify(jsonResponse), status.HTTP_200_OK