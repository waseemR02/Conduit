from bs4 import BeautifulSoup
import requests
from datetime import datetime
from flask import Flask, jsonify, Response
from flask import request as flask_req
import json


app = Flask(__name__)


@app.route("/sprintlist", methods=["GET"])
def sprintlist() -> Response:
    with open("docs/SprintsDump.json") as f:
        return jsonify(json.load(f))


@app.route("/parentItems", methods=["GET"])
def parentItems() -> Response:
    parentItems = {"parent": []}

    sprint_name = flask_req.args.get("sprint")
    if sprint_name is None:
        parentItems["parent"].append({"id": None, "url": None})
        return jsonify(parentItems)

    if sprint_name == "Sprint086":
        with open("docs/Sprint86Dump.json") as f:
            workItems = json.load(f)["workItemRelations"]
    else:
        try:
            sprints = json.loads(requests.get("http://localhost/5000/sprintlist").text)[
                "value"
            ]
            for sprint in sprints:
                if sprint["name"] == sprint_name:
                    try:
                        workItems = json.loads(requests.get(f"{sprint["url"]}").text)[
                            "workItemRelations"
                        ]
                    except requests.exceptions.RequestException as e:
                        print(e)

        except requests.exceptions.RequestException as e:
            print(e)

    for workItem in workItems:
        if workItem["rel"] is None and workItem["source"] is None:
            parentItems["parent"].append(workItem["target"])

    return jsonify(parentItems)


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
