from datetime import datetime
import requests
import json

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_api import status

import app

yammer_page = Blueprint('yammer_page', __name__)

clientId = "3rkYgsKyVGRCffhqjtmFjg"
clientSecret = "Fs5GnZgWTIjVIxdl9FRlmycJY38ARSArAOKrAS4WM"


@yammer_page.route('/yammer/oauth', methods=["GET"])
def oauth():
    redirectUri = "http://localhost:3000/services?from=yammer"

    return jsonify("https://www.yammer.com/oauth2/authorize?client_id=" + clientId + "&response_type=code&redirect_uri=" + redirectUri)


@yammer_page.route('/yammer/oauth2', methods=["POST"])
def oauth2():
    body = request.form.to_dict()

    code = body["url"].split("?")[1].split("&")[0].split("=")[1]
    yammerResponse = json.loads(requests.get(
        "https://www.yammer.com/oauth2/access_token.json?client_id=" + clientId + "&client_secret=" + clientSecret + "&code=" + code).content)
    app.setServiceAccesToken(
        body["userId"], "yammer", yammerResponse["access_token"]["token"])
    return jsonify("Oauth2: OK"), status.HTTP_200_OK


@yammer_page.route('/yammer/group_message', methods=["POST"])
def group_message():
    params = json.loads(dict(request.form)["params"][0])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "yammer")
    jsonResponse = {
        "direction": "column",
        "items": []
    }

    groupId = params["url"].split('?')[1].split('&')[1].split('=')[1]

    yammerResponse = json.loads(requests.get(
        "https://www.yammer.com/api/v1/messages/in_group/" + groupId + ".json?threaded=true", headers={"Authorization": "Bearer " + accessToken}).content)
    for message in yammerResponse["messages"]:
        if "title" in message:
            jsonResponse["items"].append({"value": message["title"][:70] + "..." if len(
                message["title"]) >= 70 else message["title"], "link": message["web_url"]})
        else:
            jsonResponse["items"].append({"value": message["body"]["plain"][:70] + "..." if len(
                message["body"]["plain"]) >= 70 else message["body"]["plain"], "link": message["web_url"]})
        if len(jsonResponse["items"]) == int(params["number"]):
            break
    return jsonify(jsonResponse), status.HTTP_200_OK


@yammer_page.route('/yammer/group_list', methods=["POST"])
def group_list():
    params = json.loads(dict(request.form)["params"][0])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "yammer")
    jsonResponse = {
        "direction": "column",
        "items": []
    }

    yammerResponse = json.loads(requests.get(
        "https://www.yammer.com/api/v1/users/by_email.json?email=" + params["email"], headers={"Authorization": "Bearer " + accessToken}).content)
    userId = yammerResponse[0]["id"]

    yammerResponse = json.loads(requests.get(
        "https://www.yammer.com/api/v1/groups/for_user/" + str(userId) + ".json", headers={"Authorization": "Bearer " + accessToken}).content)
    for group in yammerResponse:
        newGroup = {
            "value": {
                "direction": "row",
                "items": [
                    {"span": 2, "value": group["full_name"]},
                    {"value": str(group["stats"]["members"]) + " members"}
                ]
            },
            "link": group["web_url"]
        }
        jsonResponse["items"].append(newGroup)
    return jsonify(jsonResponse), status.HTTP_200_OK