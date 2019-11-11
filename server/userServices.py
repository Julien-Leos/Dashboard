import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app


userServices_page = Blueprint('userServices_page', __name__)


@userServices_page.route('/users/<userId>/services', defaults={'serviceId': None}, methods=["GET", "POST"])
@userServices_page.route('/users/<userId>/services/<serviceId>', methods=["GET", "PUT", "DELETE"])
def userServices(userId, serviceId):
    form = request.form.to_dict(flat=True)
    users = app.getDict(database.child('users'))
    actualUser = app.getActualUser(request.headers.get("Authorization"), users)

    params = {
        "name": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "accessToken": {
            "type": str,
            "mandatory": True,
            "default": None
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

    user = database.child('users').child(userId)
    if user.get().val() == None:
        return jsonify({"message": "Error: user '" + userId + "' do not exist."}), status.HTTP_400_BAD_REQUEST
    userServices = app.getDict(database.child(
        'users').child(userId).child('services'))

    with open('about.json', 'r') as json_file:
        jsonData = json.load(json_file)["server"]["services"]

    if request.method == "GET" and not serviceId:
        return List(userServices, userId, actualUser)
    elif request.method == "GET" and serviceId:
        return Get(userServices, userId, serviceId, actualUser)
    elif request.method == "POST" and not serviceId:
        return Post(userServices, form, params, jsonData, userId, actualUser)
    elif request.method == "PUT" and serviceId:
        return Put(userServices, form, jsonData, userId, serviceId, actualUser)
    elif request.method == "DELETE" and serviceId:
        return Delete(userServices, userId, serviceId, actualUser)


def List(userServices, userId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get list of other user's services"}), status.HTTP_400_BAD_REQUEST

    return jsonify({"message": "User's services successfully getted", "data": {"services": userServices}}), status.HTTP_200_OK


def Get(userServices, userId, serviceId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get other user's service"}), status.HTTP_400_BAD_REQUEST

    if serviceId in userServices:
        userService = userServices[serviceId]
        return jsonify({"message": "User's service '" + userService["name"] + "' successfully getted", "data": {"services": userServices[serviceId]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(userServices, form, params, jsonData, userId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a user's service"}), status.HTTP_400_BAD_REQUEST

    serviceExist = False
    for serviceJsonData in jsonData:
        if serviceJsonData["name"].lower() == form["name"].lower():
            serviceExist = True
    if not serviceExist:
        return jsonify({"message": "Error: Service '" + form["name"].lower() + "' do not exist."}), status.HTTP_400_BAD_REQUEST

    for userService in userServices.values():
        if userService["name"].lower() == form["name"].lower():
            return jsonify({"message": "Error: User's service '" + form["name"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]
    form["widgets"] = ""

    database.child('users').child(userId).child('services').push(form)
    return jsonify({"message": "User's service '" + form["name"] + "' successfully connected.", "data": {"services": form}}), status.HTTP_200_OK


def Put(userServices, form, jsonData, userId, serviceId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update a user's service"}), status.HTTP_400_BAD_REQUEST

    if "name" in form:
        serviceExist = False
        for serviceJsonData in jsonData:
            if serviceJsonData["name"].lower() == form["name"].lower():
                serviceExist = True
        if not serviceExist:
            return jsonify({"message": "Error: Service '" + form["name"].lower() + "' do not exist."}), status.HTTP_400_BAD_REQUEST

        for userService in userServices.values():
            if userService["name"].lower() == form["name"].lower():
                return jsonify({"message": "Error: User's service '" + form["name"].lower() + "' already exist"}), status.HTTP_400_BAD_REQUEST

    if serviceId in userServices:
        userService = userServices[serviceId]
        database.child('users').child(userId).child(
            'services').child(serviceId).update(form)
        return jsonify({"message": "User's service '" + userService["name"] + "' successfully updated.", "data": {"services": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(userServices, userId, serviceId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete a user's service"}), status.HTTP_400_BAD_REQUEST

    if serviceId in userServices:
        userService = userServices[serviceId]
        database.child('users').child(userId).child(
            'services').child(serviceId).remove()
        userServices.pop(serviceId)
        if len(userServices) == 0:
            database.child('users').child(userId).update({"services": ""})
        return jsonify({"message": "User's service '" + userService["name"] + "' successfully disconnected.", "data": {"services": userServices}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST
