from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

userServices_page = Blueprint('userServices_page', __name__)


@userServices_page.route('/user/<userId>/services', defaults={'id': None}, methods=["GET", "POST"])
@userServices_page.route('/user/<userId>/services/<id>', methods=["GET", "PUT", "DELETE"])
def services(userId, id):
    form = request.form.to_dict(flat=True)
    users = app.getDict(database.child('users'))
    actualUser = app.getActualUser(request.headers.get("Authorization"), users)

    params = {
        "id": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "widgets": {
            "type": dict,
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

    userServices = app.getDict(database.child('users').child(userId).child('services'))

    if request.method == "GET" and not id:
        return List(userServices)
    elif request.method == "GET" and id:
        return Get(userServices, id)
    elif request.method == "POST" and not id:
        return Post(userServices, form, params, actualUser)
    elif request.method == "PUT" and id:
        return Put(userServices, form, id, actualUser)
    elif request.method == "DELETE" and id:
        return Delete(userServices, form, id, actualUser)


def List(userServices):
    return jsonify({"message": "User's services successfully getted", "data": {"userServices": userServices}}), status.HTTP_200_OK


def Get(userServices, id):
    if id in userServices:
        return jsonify({"message": "User's service '" + id + "' successfully getted", "data": {"userServices": userServices[id]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's service '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(userServices, form, params, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a user's service"}), status.HTTP_400_BAD_REQUEST

    for userService in userServices.values():
        if userService["name"].lower() == form["name"].lower():
            return jsonify({"message": "Error: User's service '" + form["name"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]

    database.child('services').push(form)
    return jsonify({"message": "User's service '" + form["name"] + "' successfully created", "data": {"userService": form}}), status.HTTP_200_OK


def Put(userServices, form, id, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update a user's service"}), status.HTTP_400_BAD_REQUEST

    if id in userServices:
        database.child('services').child(id).update(form)
        return jsonify({"message": "User's service '" + id + "' successfully updated.", "data": {"userService": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's service '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(userServices, form, id, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete a user's service"}), status.HTTP_400_BAD_REQUEST

    if id in userServices:
        database.child('services').child(id).remove()
        userServices.pop(id)
        return jsonify({"message": "User's service '" + id + "' successfully removed.", "data": {"userService": userServices}}), status.HTTP_200_OK
    return jsonify({"message": "Error: User's service '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST
