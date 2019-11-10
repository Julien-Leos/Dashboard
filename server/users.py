from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

users_page = Blueprint('users_page', __name__)


@users_page.route('/users', defaults={'userId': None}, methods=["GET", "POST"])
@users_page.route('/users/<userId>', methods=["GET", "PUT", "DELETE"])
def users(userId):
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

    if request.method == "GET" and not userId:
        return List(users, actualUser)
    elif request.method == "GET" and userId:
        return Get(users, userId, actualUser)
    elif request.method == "POST" and not userId:
        return Post(users, form, params, actualUser)
    elif request.method == "PUT" and userId:
        return Put(users, form, userId, actualUser)
    elif request.method == "DELETE" and userId:
        return Delete(users, userId, actualUser)


def List(users, actualUser):
    # TO-DO: Commented because a non-admin user have to get all the users to found his
    # own key. I have to find a way to return the user's key when creating it.
    #
    # if not actualUser["value"]["isAdmin"]:
    #     return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get list of all users"}), status.HTTP_400_BAD_REQUEST

    return jsonify({"message": "users successfully getted", "data": {"users": users}}), status.HTTP_200_OK


def Get(users, userId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot get an other user"}), status.HTTP_400_BAD_REQUEST

    if userId in users:
        user = users[userId]
        return jsonify({"message": "user '" + user["email"] + "' successfully getted", "data": {"users": users[userId]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: user '" + userId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(users, form, params, actualUser):
    if "isAdmin" in form and form["isAdmin"] == "true" and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a user with administrator permissions"}), status.HTTP_400_BAD_REQUEST

    for user in users.values():
        if user["email"].lower() == form["email"].lower():
            return jsonify({"message": "Error: user '" + form["email"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]
    form["services"] = ""

    database.child('users').push(form)
    return jsonify({"message": "user '" + form["email"] + "' successfully created", "data": {"user": form}}), status.HTTP_200_OK


def Put(users, form, userId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update an other user"}), status.HTTP_400_BAD_REQUEST

    if "email" in form:
        for user in users.values():
            if user["email"].lower() == form["email"].lower():
                return jsonify({"message": "Error: user '" + form["email"] + "' already exist"}), status.HTTP_400_BAD_REQUEST

    if userId in users:
        user = users[userId]
        if "isAdmin" in form and not actualUser["value"]["isAdmin"]:
            return jsonify({"message": "Error: user '" + userId + "' cannot set himself as administrator"}), status.HTTP_400_BAD_REQUEST
        database.child('users').child(userId).update(form)
        return jsonify({"message": "user '" + user["email"] + "' successfully updated.", "data": {"user": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: user '" + userId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(users, userId, actualUser):
    if actualUser["key"] != userId and not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete an other user"}), status.HTTP_400_BAD_REQUEST

    if userId in users:
        user = users[userId]
        database.child('users').child(userId).remove()
        users.pop(userId)
        if len(users) == 0:
            database.update({"users": ""})
        return jsonify({"message": "user '" + user["emial"] + "' successfully removed.", "data": {"user": users}}), status.HTTP_200_OK
    return jsonify({"message": "Error: user '" + userId + "' do not exist."}), status.HTTP_400_BAD_REQUEST
