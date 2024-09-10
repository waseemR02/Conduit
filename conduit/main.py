from bs4 import BeautifulSoup
import requests
from datetime import datetime
from flask import Flask, jsonify, Response
import json


app = Flask(__name__)


@app.route("/sprintlist", methods=["GET"])
def sprintlist() -> Response:
    with open("docs/SprintsDump.json") as f:
        return jsonify(json.load(f))


@app.route("/4136d780-1d04-4709-a4b5-81f89e471ec6", methods=["GET"])
def sprintdata() -> Response:
    with open("docs/Sprint86Dump.json") as f:
        return jsonify(json.load(f))


@app.route("/parentTask/2539400", methods=["GET"])
def parentTask() -> Response:
    with open("docs/ParentTask1Sprint86Dump.json") as f:
        return jsonify(json.load(f))


@app.route("/rss", methods=["GET"])
def rss() -> Response:
    rss_feed = requests.get("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    rss_text = rss_feed.text
    soup = BeautifulSoup(rss_text, "xml")
    items = soup.findAll("item")

    data = {
        "data": [
            {
                "title": item.title.text,
                "source": item.source.text,
                "timestamp": datetime.now().timestamp(),
            }
            for item in items
        ]
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
