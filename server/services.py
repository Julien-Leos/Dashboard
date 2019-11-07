from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

services_page = Blueprint('services_page', __name__)


@services_page.route('/services', defaults={'id': None}, methods=["GET", "POST"])
@services_page.route('/services/<id>', methods=["GET", "PUT", "DELETE"])
def services(id):
    headers = request.headers
    form = request.form.to_dict()
    users = app.getChildItems(database.child('users'))

    params = {
        "name": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "isOauth": {
            "type": bool,
            "mandatory": False,
            "default": False
        },
        "color": {
            "type": str,
            "mandatory": False,
            "default": "FFFFFF"
        }
    }

    if not app.checkAccessToken(headers, users):
        return jsonify({"message": "User not authorized"}), status.HTTP_401_UNAUTHORIZED

    if request.method != "GET":
        paramError = app.checkAPIParams(form, params)
        if paramError != None:
            return paramError

    if request.method == "GET" and not id:
        return servicesList()
    elif request.method == "GET" and id:
        return servicesGet(form, id)
    elif request.method == "POST":
        return servicesPost(form, params)
    elif request.method == "PUT":
        return servicesPut(form)
    elif request.method == "DELETE":
        return servicesDelete(form)


def servicesList():
    services = app.getChildItems(database.child('services'))
    return jsonify({"message": "Services successfully getted", "data": {"services": services}}), status.HTTP_200_OK


def servicesGet(form, id):
    services = app.getChildItems(database.child('services'))
    if id in services:
        return jsonify({"message": "Service '" + services[id]["name"] + "' successfully getted", "data": {"services": services[id]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + services[id]["name"] + "' do not exist."}), status.HTTP_400_BAD_REQUEST
    
    # for service in services:
    #     if service[1]["name"].lower() == form["name"].lower():
    #         return jsonify({"message": "Service '" + form["name"] + "' successfully getted", "data": {"services": service}}), status.HTTP_200_OK
    # return jsonify({"message": "Error: Service '" + form["name"] + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def servicesPost(form, params):
    services = app.getChildItems(database.child('services'))
    for service in services:
        if service[1]["name"].lower() == form["name"].lower():
            return jsonify({"message": "Error: Service '" + form["name"] + "' already exist"}), status.HTTP_400_BAD_REQUEST
    
    for param in params.items():
        if not param[0] in form:
            form[str(param[0])] = param[1]["default"]
    database.child('services').push(form)
    return jsonify({"message": "Service '" + form["name"] + "' successfully created", "data": {"service": form}}), status.HTTP_200_OK


def servicesPut(form):
    services = app.getChildItems(database.child('services'))

    for service in services:
        if service[1]["name"].lower() == form["name"].lower():
            database.child('services').child(service[0]).update(form)
            return jsonify({"message": "Service '" + form["name"] + "' successfully updated.", "data": {"service": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + form["name"] + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def servicesDelete(form):
    services = app.getChildItems(database.child('services'))

    for service in services:
        if service[1]["name"].lower() == form["name"].lower():
            database.child('services').child(service[0]).remove()
            services.remove(service)
            return jsonify({"message": "Service '" + form["name"] + "' successfully removed.", "data": {"service": services}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + form["name"] + "' do not exist."}), status.HTTP_400_BAD_REQUEST
