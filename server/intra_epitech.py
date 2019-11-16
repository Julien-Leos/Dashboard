from datetime import datetime
import requests
import math
import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

import app

intra_epitech_page = Blueprint('intra_epitech_page', __name__)


@intra_epitech_page.route('/intra_epitech/oauth', methods=["GET"])
def oauth():
    redirectUri = "http://localhost:3000/services?from=intra_epitech"

    return jsonify("http://localhost:3000/other/intra_epitech/autologin?redirect_uri=" + redirectUri)


@intra_epitech_page.route('/intra_epitech/oauth2', methods=["POST"])
def oauth2():
    body = request.form.to_dict()

    accessToken = body["url"].split("#")[1].split("&")[0].split("=")[1]
    app.setServiceAccesToken(body["userId"], "intra_epitech", accessToken)
    return jsonify("Oauth2: OK"), status.HTTP_200_OK

@intra_epitech_page.route('/intra_epitech/unregistered_instances', methods=["POST"])
def unregistered_instances():
    params = json.loads(dict(request.form)["params"])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["instance_type"]},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/?format=json").content)
    for entity in intraResponse["board"][params["instance_type"]]:
        if entity["date_inscription"] != False:
            dateTimeOffset = datetime.strptime(
                entity["date_inscription"], "%d/%m/%Y, %H:%M") - datetime.now()
            nbDaysOffset = dateTimeOffset.total_seconds() / 3600 / 24
            newEntity = {
                "direction": "row",
                "items": [
                    {"span": 2, "value": entity["title"]},
                    {"value": str(int(nbDaysOffset)) + " days"}
                ]
            }
            jsonResponse["items"][1]["value"]["items"].append(
                {"value": newEntity})
    return jsonify(jsonResponse), status.HTTP_200_OK


@intra_epitech_page.route('/intra_epitech/binome_projects', methods=["POST"])
def binome_projects():
    params = json.loads(dict(request.form)["params"])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["firstname"].capitalize(
            ) + " " + params["lastname"].capitalize()},
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
        if binome["login"] == params["firstname"].lower() + "." + params["lastname"].lower() + "@epitech.eu":
            projects = binome["activities"].split(',')
            for project in projects:
                jsonResponse["items"][1]["value"]["items"].append(
                    {"value": project})
    return jsonify(jsonResponse), status.HTTP_200_OK


@intra_epitech_page.route('/intra_epitech/year_grades', methods=["POST"])
def year_grades():
    params = json.loads(dict(request.form)["params"])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["year"]},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/user?format=json").content)
    userLogin = intraResponse["login"]

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/user/" + userLogin + "/notes?format=json").content)
    for module in intraResponse["modules"]:
        if str(module["scolaryear"]) == params["year"] and module["grade"] == params["grade"]:
            newGrade = {
                "direction": "row",
                "items": [
                    {"span": 2, "value": module["title"]},
                    {"value": "Grade " + module["grade"]}
                ]
            }
            jsonResponse["items"][1]["value"]["items"].append(
                {"value": newGrade})
    return jsonify(jsonResponse), status.HTTP_200_OK


@intra_epitech_page.route('/intra_epitech/netsoul', methods=["POST"])
def netsoul():
    params = json.loads(dict(request.form)["params"])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["method"].capitalize()},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/user?format=json").content)
    userLogin = intraResponse["login"]

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/user/" + userLogin + "/netsoul?format=json").content)

    startDateTimeStamp = datetime.strptime(params["duration"][0], '%Y-%m-%d').timestamp()
    endDateTimeStamp = datetime.strptime(params["duration"][1], '%Y-%m-%d').timestamp()

    startDateIndex = 0
    endDateIndex = len(intraResponse) - 1

    for (index, netsoul) in enumerate(intraResponse):
        if netsoul[0] == int(startDateTimeStamp):
            startDateIndex = index
        elif netsoul[0] == int(endDateTimeStamp):
            endDateIndex = index
            break

    netsoulList = intraResponse[startDateIndex:endDateIndex + 1]
    netsoulList.reverse()

    if params["method"] == "daily":
        for i in range(0, len(netsoulList), 1):
            date = datetime.fromtimestamp(
                netsoulList[i][0]).strftime("%Y-%m-%d")
            newNetsoul = {"direction": "row", "items": [
                {"span": 2, "value": date},
                {"value": str(round(netsoulList[i][1] / 3600)) + " hours"}]}
            jsonResponse["items"][1]["value"]["items"].append(
                {"value": newNetsoul})
    elif params["method"] == "weekly":
        for i in range(0, len(netsoulList), 7):
            lastDate = datetime.fromtimestamp(
                netsoulList[i][0]).strftime("%Y-%m-%d")
            firstDate = datetime.fromtimestamp(netsoulList[i + 6 if i + 6 < len(
                netsoulList) else len(netsoulList) - 1][0]).strftime("%Y-%m-%d")
            newNetsoul = {"direction": "row", "items": [
                {"span": 2, "value": firstDate + " - " + lastDate},
                {"value": str(round(sum([netsoulList[i + x][1] if i + x < len(netsoulList) else 0 for x in range(0, 7)]) / 3600)) + " hours"}]}
            jsonResponse["items"][1]["value"]["items"].append(
                {"value": newNetsoul})
    elif params["method"] == "monthly":
        print("TOTO")
        for i in range(0, len(netsoulList), 31):
            lastDate = datetime.fromtimestamp(
                netsoulList[i][0]).strftime("%Y-%m-%d")
            firstDate = datetime.fromtimestamp(netsoulList[i + 29 if i + 29 < len(
                netsoulList) else len(netsoulList) - 1][0]).strftime("%Y-%m-%d")
            newNetsoul = {"direction": "row", "items": [
                {"span": 2, "value": firstDate + " - " + lastDate},
                {"value": str(round(sum([netsoulList[i + x][1] if i + x < len(netsoulList) else 0 for x in range(0, 31)]) / 3600)) + " hours"}]}
            jsonResponse["items"][1]["value"]["items"].append(
                {"value": newNetsoul})
    return jsonify(jsonResponse), status.HTTP_200_OK


@intra_epitech_page.route('/intra_epitech/activities', methods=["POST"])
def activities():
    params = json.loads(dict(request.form)["params"])
    userId = dict(request.form)["userId"][0]
    accessToken = app.getServiceAccesToken(userId, "intra_epitech")
    jsonResponse = {
        "direction": "column",
        "items": [
            {"value": params["date"]},
            {"span": 8, "value": {
                "direction": "column", "items": []
            }}
        ]
    }

    intraResponse = json.loads(requests.get(
        "https://intra.epitech.eu/" + accessToken + "/planning/load?format=json&start=" + params["date"] + "&end=" + params["date"]).content)
    for activity in intraResponse:
        if activity["event_registered"] != False:
            startHour = activity["start"].split(' ')[1].split(':')
            newActivity = {
                "direction": "row",
                "items": [
                    {"span": 2, "value": activity["titlemodule"]},
                    {"span": 2, "value": activity["acti_title"]},
                    {"value": ":".join([startHour[0], startHour[1]])}
                ]
            }
            jsonResponse["items"][1]["value"]["items"].append(
                {"value": newActivity})
    jsonResponse["items"][1]["value"]["items"].sort(
        key=lambda x: x["value"]["items"][2]["value"])
    return jsonify(jsonResponse), status.HTTP_200_OK
