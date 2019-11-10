import requests

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

import xml.etree.ElementTree as ET

rss_page = Blueprint('rss_page', __name__)


@rss_page.route('/rss/article_list', methods=["GET"])
def article_list():
    if request.method == "GET":
        body = request.form
        response = {
            "direction": "column",
            "items": []
        }

        rssFlux = requests.get('https://www.lemonde.fr/rss/une.xml').content
        channel = ET.fromstring(rssFlux)[0]
        for item in channel:
            if item.tag == "item":
                article = {}
                for attrib in item:
                    if attrib.tag == "title":
                        article["value"] = attrib.text
                    if attrib.tag == "link":
                        article["link"] = attrib.text
                response["items"].append(article)
        return jsonify(response)
