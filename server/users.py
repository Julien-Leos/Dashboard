from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

users_page = Blueprint('users_page', __name__)


@users_page.route('/users', defaults={'id': None}, methods=["GET", "POST"])
@users_page.route('/users/<id>', methods=["GET", "PUT", "DELETE"])
def users(id):
    form = request.form.to_dict(flat=True)
    users = app.getDict(database.child('users'))
    actualUser = app.getActualUser(request.headers.get("Authorization"), users)

    params = {
        "email": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "password": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "isAdmin": {
            "type": bool,
            "mandatory": False,
            "default": False
        },
        "accessToken": {
            "type": str,
            "mandatory": False,
            "default": ""
        },
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

    if request.method == "GET" and not id:
        return List(users, actualUser)
    elif request.method == "GET" and id:
        return Get(users, id, actualUser)
    elif request.method == "POST" and not id:
        return Post(users, form, params, actualUser)
    elif request.method == "PUT" and id:
        return Put(users, form, id, actualUser)
    elif request.method == "DELETE" and id:
        return Delete(users, form, id, actualUser)


def List(users, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get list of all users"}), status.HTTP_400_BAD_REQUEST
    
    return jsonify({"message": "users successfully getted", "data": {"users": users}}), status.HTTP_200_OK


def Get(users, id, actualUser):
    if actualUser["key"] != id and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get an other user"}), status.HTTP_400_BAD_REQUEST
    
    if id in users:
        return jsonify({"message": "user '" + id + "' successfully getted", "data": {"users": users[id]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: user '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(users, form, params, actualUser):
    for user in users.values():
        if user["email"].lower() == form["email"].lower():
            return jsonify({"message": "Error: user '" + form["email"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    if "isAdmin" in form and form["isAdmin"] == "true" and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a user with administrator permissions"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]

    database.child('users').push(form)
    return jsonify({"message": "user '" + form["email"] + "' successfully created", "data": {"user": form}}), status.HTTP_200_OK


def Put(users, form, id, actualUser):
    if actualUser["key"] != id and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update an other user"}), status.HTTP_400_BAD_REQUEST

    if id in users:
        if "isAdmin" in form and not actualUser["value"]["isAdmin"]:
            return jsonify({"message": "Error: user '" + id + "' cannot set himself as administrator"}), status.HTTP_400_BAD_REQUEST
        database.child('users').child(id).update(form)
        return jsonify({"message": "user '" + id + "' successfully updated.", "data": {"user": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: user '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(users, form, id, actualUser):
    if actualUser["key"] != id and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete an other user"}), status.HTTP_400_BAD_REQUEST

    if id in users:
        database.child('users').child(id).remove()
        users.pop(id)
        return jsonify({"message": "user '" + id + "' successfully removed.", "data": {"user": users}}), status.HTTP_200_OK
    return jsonify({"message": "Error: user '" + id + "' do not exist."}), status.HTTP_400_BAD_REQUEST
