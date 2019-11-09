import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app


userWidgets_page = Blueprint('userWidgets_page', __name__)


@userWidgets_page.route('/users/<userId>/services/<serviceId>/widgets', defaults={'widgetId': None}, methods=["GET", "POST"])
@userWidgets_page.route('/users/<userId>/services/<serviceId>/widgets/<widgetId>', methods=["GET", "PUT", "DELETE"])
def userWidgets(userId, serviceId, widgetId):
    form = request.form.to_dict(flat=True)
    users = app.getDict(database.child('users'))
    actualUser = app.getActualUser(request.headers.get("Authorization"), users)

    params = {
        "name": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "x": {
            "type": int,
            "mandatory": True,
            "default": None
        },
        "y": {
            "type": int,
            "mandatory": True,
            "default": None
        },
        "w": {
            "type": int,
            "mandatory": False,
            "default": 4
        },
        "h": {
            "type": int,
            "mandatory": False,
            "default": 7
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

    userService = database.child('users').child(
        userId).child('services').child(serviceId)
    if userService.get().val() == None:
        return jsonify({"message": "Error: user's service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST
    userWidgets = app.getDict(database.child('users').child(
        userId).child('services').child(serviceId).child('widgets'))

    serviceName = app.getDict(database.child('users').child(userId).child(
        'services').child(serviceId))["name"]
    with open('about.json', 'r') as json_file:
        jsonData = json.load(json_file)["server"]
        for service in jsonData["services"]:
            if service["name"].lower() == serviceName.lower():
                jsonData = service["widgets"]

    if request.method == "GET" and not widgetId:
        return List(userWidgets, userId, actualUser)
    elif request.method == "GET" and widgetId:
        return Get(userWidgets, userId, widgetId, actualUser)
    elif request.method == "POST" and not widgetId:
        return Post(userWidgets, form, params, jsonData, userId, serviceId, actualUser)
    elif request.method == "PUT" and widgetId:
        return Put(userWidgets, form, jsonData, userId, serviceId, widgetId, actualUser)
    elif request.method == "DELETE" and widgetId:
        return Delete(userWidgets, userId, serviceId, widgetId, actualUser)


def List(userWidgets, userId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get list of other user's widgets"}), status.HTTP_400_BAD_REQUEST

    return jsonify({"message": "User's widgets successfully getted", "data": {"widgets": userWidgets}}), status.HTTP_200_OK


def Get(userWidgets, userId, widgetId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get other user's widgets"}), status.HTTP_400_BAD_REQUEST

    if widgetId in userWidgets:
        userWidget = userWidgets[widgetId]
        return jsonify({"message": "User's widget '" + userWidget["name"] + "' successfully getted", "data": {"widgets": userWidgets[widgetId]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's widget '" + widgetId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(userWidgets, form, params, jsonData, userId, serviceId, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a user's widget"}), status.HTTP_400_BAD_REQUEST

    widgetExist = False
    for widgetJsonData in jsonData:
        if widgetJsonData["name"].lower() == form["name"].lower():
            widgetExist = True
    if not widgetExist:
        return jsonify({"message": "Error: Widget '" + form["name"].lower() + "' do not exist."}), status.HTTP_400_BAD_REQUEST

    for userWidget in userWidgets.values():
        if userWidget["name"].lower() == form["name"].lower():
            return jsonify({"message": "Error: User's widget '" + form["name"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]

    database.child('users').child(userId).child(
        'services').child(serviceId).child('widgets').push(form)
    return jsonify({"message": "User's widget '" + form["name"] + "' successfully created", "data": {"widgets": form}}), status.HTTP_200_OK


def Put(userWidgets, form, jsonData, userId, serviceId, widgetId, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update a user's widget"}), status.HTTP_400_BAD_REQUEST

    if "name" in form:
        widgetExist = False
        for widgetJsonData in jsonData:
            if widgetJsonData["name"].lower() == form["name"].lower():
                widgetExist = True
        if not widgetExist:
            return jsonify({"message": "Error: Widget '" + form["name"].lower() + "' do not exist."}), status.HTTP_400_BAD_REQUEST

        for userWidget in userWidgets.values():
            if userWidget["name"].lower() == form["name"].lower():
                return jsonify({"message": "Error: User's widget '" + form["name"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    if widgetId in userWidgets:
        userWidget = userWidgets[widgetId]
        database.child('users').child(userId).child(
            'services').child(serviceId).child('widgets').child(widgetId).update(form)
        return jsonify({"message": "User's widget '" + userWidget["name"] + "' successfully updated.", "data": {"widgets": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's widget '" + widgetId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(userWidgets, userId, serviceId, widgetId, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete a user's widget"}), status.HTTP_400_BAD_REQUEST

    if widgetId in userWidgets:
        userWidget = userWidgets[widgetId]
        database.child('users').child(userId).child(
            'services').child(serviceId).child('widgets').child(widgetId).remove()
        userWidgets.pop(widgetId)
        if len(userWidgets) == 0:
            database.child('users').child(userId).child(
                'services').child(serviceId).update({"widgets": ""})
        return jsonify({"message": "User's widget '" + userWidget["name"] + "' successfully removed.", "data": {"widgets": userWidgets}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's widget '" + widgetId + "' do not exist."}), status.HTTP_400_BAD_REQUEST
