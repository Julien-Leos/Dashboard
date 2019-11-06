from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

services_page = Blueprint('services_page', __name__)


@services_page.route('/services', defaults={'name': None})
@services_page.route('/services/<name>', methods=["GET", "POST", "PUT", "DELETE"])
def services(name):
    header = request.headers
    body = request.form
    users = app.getChildItems(database.child('users'))

    if not app.checkAccessToken(header, users):
        return jsonify({"message": "User not authorized"}), status.HTTP_401_UNAUTHORIZED

    if request.method == "GET" and not name:
        services = app.getChildItems(database.child('services'))
        return jsonify({"message": "Services successfully getted", "data": {"services": services}}), status.HTTP_200_OK
    elif request.method == "GET" and name:
        services = app.getChildItems(database.child('services'))
        for service in services:
            if service[1]["name"].lower() == name.lower():
                return jsonify({"message": "Service " + name + " successfully getted", "data": {"services": service}}), status.HTTP_200_OK
        return jsonify({"message": "Service " + name + " do not exist."}), status.HTTP_400_BAD_REQUEST
    elif request.method == "POST":
        newService = {"name": name,
                      "isOauth": body["isOauth"], "color": body["color"]}
        database.child('services').push(newService)
        return jsonify({"message": "Service " + name + " successfully created", "data": {"service": newService}}), status.HTTP_200_OK
    elif request.method == "PUT":
        services = app.getChildItems(database.child('services'))
        for service in services:
            if service[1]["name"].lower() == name.lower():
                updateService = {}
                for item in body.to_dict().items():
                    updateService[item[0]] = item[1]
                database.child('services').child(service[0]).update(updateService)
                return jsonify({"message": "Service " + name + " successfully updated.", "data": {"service": updateService}}), status.HTTP_200_OK
        return jsonify({"message": "Service " + name + " do not exist."}), status.HTTP_400_BAD_REQUEST
    elif request.method == "DELETE":
        services = app.getChildItems(database.child('services'))
        for service in services:
            if service[1]["name"].lower() == name.lower():
                database.child('services').child(service[0]).remove()
                services.remove(service)
                return jsonify({"message": "Service " + name + " successfully removed.", "data": {"service": services}}), status.HTTP_200_OK
        return jsonify({"message": "Service " + name + " do not exist."}), status.HTTP_400_BAD_REQUEST