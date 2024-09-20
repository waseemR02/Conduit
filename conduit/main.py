from bs4 import BeautifulSoup
import requests
from datetime import datetime
from flask import Flask, jsonify, Response
from flask import request as flask_req
import json


app = Flask(__name__)


@app.route("/sprintlist", methods=["GET"])
def sprintlist() -> Response:
    # TODO: Change file operation block to GET req from Azure
    with open("docs/SprintsDump.json") as f:
        return jsonify(json.load(f))


@app.route("/parentItems", methods=["GET"])
def parentItems() -> Response:
    parentItems = {"parent": []}

    sprint_name = flask_req.args.get("sprint")
    if sprint_name is None:
        parentItems["parent"].append({"id": None, "url": None})
        return jsonify(parentItems)

    # Sample dump
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


@app.route("/parentTask", methods=["GET"])
def parentTask() -> Response:
    sprint_name = flask_req.args.get("sprint")
    parent_id = int(flask_req.args.get("parentID"))

    parent_details = dict()

    if sprint_name is None:
        return jsonify({"System.Title": "Sprint Name Error"})

    # Sample Dump
    if parent_id == 2539400:
        with open("docs/ParentTask1Sprint86Dump.json") as f:
            parent_details = json.load(f)["fields"]
    else:
        try:
            parentItems = json.loads(
                requests.get(
                    f"http://localhost:5000/parentItems?sprint={sprint_name}"
                ).text
            )["parent"]

            for parent in parentItems:
                if parent["id"] == parent_id:
                    try:
                        parent_details = json.loads(
                            requests.get(f"{parent["url"]}").text
                        )
                    except requests.exceptions.RequestException as e:
                        print(e)
                        break
        except requests.exceptions.RequestException as e:
            print(e)

    parent_details_narrow = {
        "System.Title": parent_details["System.Title"],
        "AssignedTo": parent_details["System.AssignedTo"]["displayName"],
        "System.State": parent_details["System.State"],
        "Custom.TargetVersion": parent_details["Custom.TargetVersion"],
    }

    return jsonify(parent_details_narrow)


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
