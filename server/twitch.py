from datetime import datetime
import requests
import json

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_api import status

import app

twitch_page = Blueprint('twitch_page', __name__)

clientId = "apxc8zgwnv9ggecemvoesem2u484i5"


@twitch_page.route('/twitch/oauth', methods=["GET"])
def oauth():
    redirectUri = "http://localhost:3000/services?from=twitch"
    scope = "user:edit+moderation:read"

    return jsonify("https://id.twitch.tv/oauth2/authorize?client_id=" + clientId + "&redirect_uri=" + redirectUri + "&response_type=token&scope=" + scope)


@twitch_page.route('/twitch/oauth2', methods=["POST"])
def oauth2():
    body = request.form.to_dict()

    accessToken = body["url"].split("#")[1].split("&")[0].split("=")[1]
    app.setServiceAccesToken(body["userId"], "twitch", accessToken)
    return jsonify("Oauth2: OK"), status.HTTP_200_OK

@twitch_page.route('/twitch/stream_viewers', methods=["POST"])
def stream_viewers():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": [{"value": params["streamer"]}]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/streams?user_login=" + params["streamer"], headers={"Client-ID": clientId}).content)
    jsonResponse["items"].append(
        {"span": 2, "value": str(twitchResponse["data"][0]["viewer_count"]) + " viewers"})
    return jsonify(jsonResponse), status.HTTP_200_OK


@twitch_page.route('/twitch/best_streams_for_game', methods=["POST"])
def best_streams_for_game():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["game"]},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/games?name=" + params["game"], headers={"Client-ID": clientId}).content)
    gameId = twitchResponse["data"][0]["id"]
    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/streams?game_id=" + gameId, headers={"Client-ID": clientId}).content)
    for stream in twitchResponse["data"]:
        newStream = {
            "direction": "row",
            "items": [
                {"span": 2, "value": stream["user_name"]},
                {"value": stream["viewer_count"]}
            ]
        }
        jsonResponse["items"][1]["value"]["items"].append(
            {"value": newStream, "link": "https://www.twitch.tv/" + stream["user_name"]})
        if len(jsonResponse["items"][1]["value"]["items"]) == int(params["number"]):
            break
    return jsonify(jsonResponse), status.HTTP_200_OK


@twitch_page.route('/twitch/streamer_followers', methods=["POST"])
def streamer_followers():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": [{"value": params["streamer"]}]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users?login=" + params["streamer"], headers={"Client-ID": clientId}).content)
    streamerId = twitchResponse["data"][0]["id"]
    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users/follows?to_id=" + streamerId, headers={"Client-ID": clientId}).content)
    jsonResponse["items"].append(
        {"span": 2, "value": str(twitchResponse["total"]) + " subs"})
    return jsonify(jsonResponse), status.HTTP_200_OK


@twitch_page.route('/twitch/moderators_events', methods=["POST"])
def moderators_events():
    params = json.loads(dict(request.form)["params"][0])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "twitch")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["user"]},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users", headers={"Authorization": "Bearer " + accessToken}).content)
    broadcasterId = twitchResponse["data"][0]["id"]

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users?login=" + params["user"], headers={"Authorization": "Bearer " + accessToken}).content)
    userId = twitchResponse["data"][0]["id"]

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/moderation/moderators/events?broadcaster_id=" + broadcasterId + "&user_id=" + userId, headers={"Authorization": "Bearer " + accessToken}).content)

    for event in twitchResponse["data"]:
        eventType = ""
        if event["event_type"] == "moderation.moderator.add":
            eventType = "Rank moderator"
        elif event["event_type"] == "moderation.moderator.remove":
            eventType = "Unrank moderator"
        newEvent = {
            "direction": "row",
            "items": [
                {"span": 2, "value": datetime.strptime(
                    event["event_timestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")},
                {"value": eventType}
            ]
        }
        jsonResponse["items"][1]["value"]["items"].append({"value": newEvent})

    return jsonify(jsonResponse), status.HTTP_200_OK


@twitch_page.route('/twitch/ban_events', methods=["POST"])
def ban_events():
    params = json.loads(dict(request.form)["params"][0])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "twitch")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["user"]},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users", headers={"Authorization": "Bearer " + accessToken}).content)
    broadcasterId = twitchResponse["data"][0]["id"]

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/users?login=" + params["user"], headers={"Authorization": "Bearer " + accessToken}).content)
    userId = twitchResponse["data"][0]["id"]

    twitchResponse = json.loads(requests.get(
        "https://api.twitch.tv/helix/moderation/banned/events?broadcaster_id=" + broadcasterId + "&user_id=" + userId, headers={"Authorization": "Bearer " + accessToken}).content)

    for event in twitchResponse["data"]:
        eventType = ""
        if event["event_type"] == "moderation.user.ban":
            eventType = "Banned"
        elif event["event_type"] == "moderation.user.unban":
            eventType = "Unbanned"
        newEvent = {
            "direction": "row",
            "items": [
                {"span": 2, "value": datetime.strptime(
                    event["event_timestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")},
                {"value": eventType}
            ]
        }
        jsonResponse["items"][1]["value"]["items"].append({"value": newEvent})

    return jsonify(jsonResponse), status.HTTP_200_OK
