from flask import Flask
from flask_cors import CORS

from sign import sign_page
from about import about_page

app = Flask(__name__)
CORS(app)

app.register_blueprint(sign_page)
app.register_blueprint(about_page)

def getChildItems(child):
    return list(child.get().val().items())

@app.route('/')
def index():
    return "Hello World!"