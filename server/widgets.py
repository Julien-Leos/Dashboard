from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

widgets_page = Blueprint('widgets_page', __name__)


@widgets_page.route('/services/<serviceId>/widgets', defaults={'id': None}, methods=["GET", "POST"])
@widgets_page.route('/services/<serviceId>/widgets/<id>', methods=["GET", "PUT", "DELETE"])
def widgets(serviceId, id):
    form = request.form.to_dict(flat=True)
    users = app.getDict(database.child('users'))
    actualUser = app.getActualUser(request.headers.get("Authorization"), users)

    params = {
        "name": {
            "type": str,
            "mandatory": True,
            "default": None
        },
        "desc": {
            "type": str,
            "mandatory": False,
            "default": "A beautiful widget"
        },
        "params": {
            "type": dict,
            "mandatory": True,
            "default": None
        },
        "url": {
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

    widgets = app.getDict(database.child('services').child('widgets'))

    if request.method == "GET" and not id:
        return List(widgets, serviceId)
    elif request.method == "GET" and id:
        return Get(widgets, id, serviceId)
    elif request.method == "POST" and not id:
        return Post(widgets, serviceId, form, params, actualUser)
    elif request.method == "PUT" and id:
        return Put(widgets, form, id, serviceId, actualUser)
    elif request.method == "DELETE" and id:
        return Delete(widgets, form, id, serviceId, actualUser)


def List(widgets, serviceId):
    return jsonify({"message": "Widgets of service '" + serviceId + "' successfully getted", "data": {"widgets": widgets}}), status.HTTP_200_OK


def Get(widgets, id, serviceId):
    if id in widgets:
        return jsonify({"message": "Widget '" + id + "' of service '" + serviceId + "' successfully getted", "data": {"widgets": widgets[id]}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Widget '" + id + "' of service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Post(widgets, form, serviceId, params, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot create a widget"}), status.HTTP_400_BAD_REQUEST

    for widget in widgets.values():
        if widget["name"].lower() == form["name"].lower():
            return jsonify({"message": "Error: Widget '" + form["name"] + "' of service '" + serviceId + "' already exist"}), status.HTTP_400_BAD_REQUEST

    for paramName, param in params.items():
        if not paramName in form:
            form[paramName] = param["default"]

    database.child('services').child(serviceId).push(form)
    return jsonify({"message": "Widget '" + form["name"] + "' of service '" + serviceId + "' successfully created", "data": {"widget": form}}), status.HTTP_200_OK


def Put(widgets, form, id, serviceId, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot update a widget"}), status.HTTP_400_BAD_REQUEST

    if id in widgets:
        database.child('services').child(serviceId).child(id).update(form)
        return jsonify({"message": "Widget '" + id + "' of service '" + serviceId + "' successfully updated.", "data": {"widget": form}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Widget '" + id + "' of service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST


def Delete(widgets, form, id, serviceId, actualUser):
    if not actualUser["value"]["isAdmin"]:
        return jsonify({"message": "Error: user '" + actualUser["value"]["email"] + "' cannot delete a widget"}), status.HTTP_400_BAD_REQUEST

    if id in widgets:
        database.child('services').child(serviceId).child(id).remove()
        widgets.pop(id)
        return jsonify({"message": "Widget '" + id + "' of service '" + serviceId + "' successfully removed.", "data": {"widget": widgets}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Widget '" + id + "' of service '" + serviceId + "' do not exist."}), status.HTTP_400_BAD_REQUEST
