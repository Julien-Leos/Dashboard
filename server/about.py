import socket
import time
import json

from flask import Blueprint

about_page = Blueprint('about_page', __name__)


@about_page.route('/about.json')
def about():
    ip = socket.gethostbyname(socket.gethostname())
    timespent = int(time.time())
    with open('about.json', 'r') as json_file:
        data = json.load(json_file)
        data['client']['host'] = ip
        data['server']['current_time'] = timespent
    return data
