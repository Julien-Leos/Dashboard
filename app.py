import time
import json
import socket
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/about.json')
def about():
    ip = socket.gethostbyname(socket.gethostname())
    timespent = int(time.time())
    with open('about.json', 'r') as json_file:
        data = json.load(json_file)
        data['client']['host'] = ip
        data['server']['current_time'] = timespent

    return data