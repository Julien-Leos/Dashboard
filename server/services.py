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
    form = request.form.to_dict(flat=True)
    users = app.getDict(database.child('users'))
    actualUser = app.getActualUser(request.headers.get("Authorization"), users)

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

    if not actualUser:
        return jsonify({"message": "User not authorized"}), status.HTTP_401_UNAUTHORIZED

    if request.method != "GET" and request.method != "DELETE":
        paramTypeError = app.checkParamsType(form, params)
        if paramTypeError != None:
            return paramTypeError
        if request.method == "POST":
            paramMandatoryError = app.checkParamsMandatory(form, params)
            if paramMandatoryError != None:
                return paramMandatoryError

    services = app.getDict(database.child('services'))

    if request.method == "GET" and not id:
        return List(services)
    elif request.method == "GET" and id:
        return Get(services, id)
    elif request.method == "POST" and not id:
        return Post(services, form, params, actualUser)
    elif request.method == "PUT" and id:
        return Put(services, form, id, actualUser)
    elif request.method == "DELETE" and id:
        return Delete(services, form, id, actualUser)


def List(services):
    return jsonify({"message": "Services successfully getted", "data": {"services": services}}), status.HTTP_200_OK


def Get(services, id):
    if id in services:
        return jsonify({"message": "Service '" + id + "' successfully getted", "data": {"services": services[id]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(services, form, params, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a service"}), status.HTTP_400_BAD_REQUEST

    for service in services.values():
        if service["name"].lower() == form["name"].lower():
            return jsonify({"message": "Error: Service '" + form["name"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]

    database.child('services').push(form)
    return jsonify({"message": "Service '" + form["name"] + "' successfully created", "data": {"service": form}}), status.HTTP_200_OK


def Put(services, form, id, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update a service"}), status.HTTP_400_BAD_REQUEST

    if id in services:
        database.child('services').child(id).update(form)
        return jsonify({"message": "Service '" + id + "' successfully updated.", "data": {"service": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(services, form, id, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete a service"}), status.HTTP_400_BAD_REQUEST

    if id in services:
        database.child('services').child(id).remove()
        services.pop(id)
        return jsonify({"message": "Service '" + id + "' successfully removed.", "data": {"service": services}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST
