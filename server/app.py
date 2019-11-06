from flask import Flask
from flask_cors import CORS

from about import about_page
from sign import sign_page
from home import home_page
from services import services_page


app = Flask(__name__)
CORS(app)

app.register_blueprint(about_page)
app.register_blueprint(sign_page)
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


@app.route('/')
def index():
    return "Hello World!"
