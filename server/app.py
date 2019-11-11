from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_api import status

from about import about_page
from login import login_page
from users import users_page
from services import services_page
from widgets import widgets_page
from userServices import userServices_page
from userWidgets import userWidgets_page

from rss import rss_page
from twitch import twitch_page

app = Flask(__name__)
CORS(app)

app.register_blueprint(about_page)
app.register_blueprint(login_page)

app.register_blueprint(users_page)
app.register_blueprint(services_page)
app.register_blueprint(widgets_page)
app.register_blueprint(userServices_page)
app.register_blueprint(userWidgets_page)

app.register_blueprint(rss_page)
app.register_blueprint(twitch_page)


def getDict(child):
    return dict(child.get().val())


def getActualUser(accessToken, users):
    for userId, user in users.items():
        if user["accessToken"] == accessToken:
            return {"key": userId, "value": user}
    return None


def checkIfInt(param):
    try:
        int(param)
        return True
    except ValueError:
        return False


def checkIfFloat(param):
    try:
        float(param)
        return True
    except ValueError:
        return False


def checkIfObject(param):
    return isinstance(param, object)


def checkIfBool(param):
    if param.lower() == "true" or param.lower() == "false":
        return True
    return False


def checkParamsMandatory(form, params):
    paramExist = False

    for paramName, param in params.items():
        paramExist = False
        if param["mandatory"]:
            for itemName in form:
                if paramName == itemName:
                    paramExist = True
            if not paramExist:
                return jsonify({"message": "Error: Param '" + paramName + "' is mandatory and has not been found."}), status.HTTP_400_BAD_REQUEST
    return None


def checkParamsType(form, params):
    paramExist = False
    paramError = False

    for itemName, item in form.items():
        paramExist = False
        for paramName, param in params.items():
            if paramName == itemName:
                paramExist = True
                if param["type"] == int and not checkIfInt(item):
                    paramError = True
                elif param["type"] == float and not checkIfFloat(item):
                    paramError = True
                elif param["type"] == object and not checkIfObject(item):
                    paramError = True
                elif param["type"] == bool and not checkIfBool(item):
                    paramError = True
            if paramError:
                return jsonify({"message": "Error: Param '" + paramName + "' should have been of type " +
                                str(param["type"]) + " but has received '" + item + "'."}), status.HTTP_400_BAD_REQUEST
        if not paramExist:
            return jsonify({"message": "Error: Param '" + itemName + "' is not recognized and should not be sent."}), status.HTTP_400_BAD_REQUEST
    return None


@app.route('/')
def index():
    return "Hello World!"
