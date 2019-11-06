from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_api import status

from about import about_page
from login import login_page
from home import home_page
from services import services_page


app = Flask(__name__)
CORS(app)

app.register_blueprint(about_page)
app.register_blueprint(login_page)
app.register_blueprint(home_page)
app.register_blueprint(services_page)


def getChildItems(child):
    return list(child.get().val().items())


def checkAccessToken(header, users):
    accessToken = header.get("Authorization")
    userAccessToken = ""

    for user in users:
        if user[1]["accessToken"] == accessToken:
            userAccessToken = user[1]["accessToken"]
    if accessToken == userAccessToken:
        return True
    return False


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


def checkIfBool(param):
    if param.lower() == "true" or param.lower() == "false":
        return True
    return False


def checkAPIParams(form, params):
    paramExist = False
    paramError = False

    for param in params.items():
        paramExist = False
        if param[1]["mandatory"]:
            for item in form.items():
                if param[0] == item[0]:
                    paramExist = True
            if not paramExist:
                return jsonify({"message": "Error: Param '" + param[0] + "' is mandatory and has not been found."}), status.HTTP_400_BAD_REQUEST

    paramExist = False
    for item in form.items():
        paramExist = False
        for param in params.items():
            if param[0] == item[0]:
                paramExist = True
                if param[1]["type"] == int and not checkIfInt(item[1]):
                    paramError = True
                elif param[1]["type"] == float and not checkIfFloat(item[1]):
                    paramError = True
                elif param[1]["type"] == bool and not checkIfBool(item[1]):
                    paramError = True
            if paramError:
                return jsonify({"message": "Error: Param '" + param[0] + "' should have been of type " +
                                str(param[1]["type"]) + " but has received '" + item[1] + "'."}), status.HTTP_400_BAD_REQUEST
        if not paramExist:
            return jsonify({"message": "Error: Param '" + item[0] + "' is not recognized and should not be sent."}), status.HTTP_400_BAD_REQUEST
    return None

@app.route('/')
def index():
    return "Hello World!"
