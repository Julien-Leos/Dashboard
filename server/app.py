import time
import json
import socket
import pyrebase

from flask import Flask
from templates.login import login_page

app = Flask(__name__)
app.register_blueprint(login_page)

@app.route('/')
def index():
    config = {
        "apiKey": "AIzaSyBTjwyIi20T5CKnXJryAe5aJ1U6u5CHkeY",
        "authDomain": "dashboard-5d0a1.firebaseapp.com",
        "databaseURL": "https://dashboard-5d0a1.firebaseio.com",
        "storageBucket": "dashboard-5d0a1.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    test = db.child('users').child('0').get()
    return test.val()

@app.route('/about.json')
def about():
    ip = socket.gethostbyname(socket.gethostname())
    timespent = int(time.time())
    with open('server/about.json', 'r') as json_file:
        data = json.load(json_file)
        data['client']['host'] = ip
        data['server']['current_time'] = timespent
    return data