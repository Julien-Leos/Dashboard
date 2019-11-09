import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

widgets_page = Blueprint('widgets_page', __name__)


@widgets_page.route('/services/<serviceName>/widgets', defaults={'widgetName': None}, methods=["GET"])
@widgets_page.route('/services/<serviceName>/widgets/<widgetName>', methods=["GET"])
def widgets(serviceName, widgetName):
    serviceExist = False
    with open('about.json', 'r') as json_file:
        jsonData = json.load(json_file)["server"]
        for service in jsonData["services"]:
            if service["name"].lower() == serviceName.lower():
                jsonData = service["widgets"]
                serviceExist = True

    if not serviceExist:
        return jsonify({"message": "Error: Service '" + serviceName.lower() + "' do not exist."}), status.HTTP_400_BAD_REQUEST

    if request.method == "GET" and not widgetName:
        return List(jsonData)
    elif request.method == "GET" and widgetName:
        return Get(jsonData, widgetName.lower())


def List(jsonData):
    return jsonify({"message": "Widgets successfully getted", "data": {"widgets": jsonData}}), status.HTTP_200_OK


def Get(jsonData, name):
    for widget in jsonData:
        if widget["name"] == name:
            return jsonify({"message": "Widget '" + name + "' successfully getted", "data": {"widgets": widget}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Widget '" + name + "' do not exist."}), status.HTTP_400_BAD_REQUEST
