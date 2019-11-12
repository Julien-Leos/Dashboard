from datetime import datetime
import requests
import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

import app

intra_epitech_page = Blueprint('intra_epitech_page', __name__)


@intra_epitech_page.route('/intra_epitech/oauth2', methods=["GET"])
def oauth2():
    redirectUri = "http://localhost:3000/services?from=intra_epitech"

    return jsonify("http://localhost:3000/other/intra_epitech/autologin?redirect_uri=" + redirectUri)


@intra_epitech_page.route('/intra_epitech/unregistered_instances', methods=["POST"])
def unregistered_instances():
    params = json.loads(dict(request.form)["params"][0])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["instance_type"]},
            {"span": 8, "value": {
                "direction": "column", "items": [
                    {
                        "value":
                            {
                                "direction": "row",
                                "items": [
                                    {"span": 2, "value": "Instance name"},
                                    {"value": "End of inscription"}
                                ]
                            }
                    }
                ]
            }}
        ]
    }
    instanceNameMap = {
        "activities": "activites",
        "projects": "projets",
        "modules": "modules",
        "susies": "susies",
        "interships": "stages",
        "tickets": "tickets"
    }

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/?format=json").content)
    for entity in intraResponse["board"][instanceNameMap[params["instance_type"]]]:
        if entity["date_inscription"] != False:
            dateTimeOffset = datetime.strptime(entity["date_inscription"], "%d/%m/%Y, %H:%M") - datetime.now()
            nbDaysOffset = dateTimeOffset.total_seconds() / 3600 / 24
            newEntity = {
                "direction": "row",
                "items": [
                    {"span": 2, "value": entity["title"]},
                    {"value": str(int(nbDaysOffset)) + " days"}
                ]
            }
            jsonResponse["items"][1]["value"]["items"].append({"value": newEntity})
    return jsonify(jsonResponse), status.HTTP_200_OK

@intra_epitech_page.route('/intra_epitech/binome_projects', methods=["POST"])
def binome_projects():
    params = json.loads(dict(request.form)["params"][0])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": " ".join([x.capitalize() for x in params["student"].split('@')[0].split('.')])},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/user?format=json").content)
    userLogin = intraResponse["login"]

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/user/" + userLogin + "/binome?format=json").content)
    for binome in intraResponse["binomes"]:
        if binome["login"] == params["student"].split('@')[0] + "@epitech.eu":
            projects = binome["activities"].split(',')
            for project in projects:
                jsonResponse["items"][1]["value"]["items"].append({"value": project})
    return jsonify(jsonResponse), status.HTTP_200_OK