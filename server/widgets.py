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
        data = json.load(json_file)["server"]
        for service in data["services"]:
            if service["name"] == serviceName.lower():
                data = service["widgets"]
                serviceExist = True

    print(data)
    if not serviceExist:
        return jsonify({"message": "Error: Service '" + serviceName.lower() + "' do not exist."}), status.HTTP_400_BAD_REQUEST

    if request.method == "GET" and not widgetName:
        return List(data)
    elif request.method == "GET" and widgetName:
        return Get(data, widgetName.lower())


def List(data):
    return jsonify({"message": "Widgets successfully getted", "data": {"widgets": data}}), status.HTTP_200_OK


def Get(data, name):
    for widget in data:
        if widget["name"] == name:
            return jsonify({"message": "Widget '" + name + "' successfully getted", "data": {"widgets": widget}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Widget '" + name + "' do not exist."}), status.HTTP_400_BAD_REQUEST
