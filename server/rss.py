import requests
import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

import xml.etree.ElementTree as ET

rss_page = Blueprint('rss_page', __name__)


@rss_page.route('/rss/article_list', methods=["POST"])
def article_list():
    params = json.loads(dict(request.form)["params"][0])
    jsonResponse = {
        "direction": "column",
        "items": []
    }

    rssFlux = requests.get(params["link"]).content
    channel = ET.fromstring(rssFlux)[0]
    for item in channel:
        if item.tag == "item":
            article = {}
            for attrib in item:
                if attrib.tag == "title":
                    article["value"] = attrib.text
                if attrib.tag == "link":
                    article["link"] = attrib.text
            jsonResponse["items"].append(article)
            if len(jsonResponse["items"]) == int(params["number"]):
                break
    return jsonify(jsonResponse), status.HTTP_200_OK
