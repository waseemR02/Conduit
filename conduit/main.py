from bs4 import BeautifulSoup
import requests
from datetime import datetime
from flask import Flask, jsonify

class Conduit:
    def poll():
        rss_feed = requests.get("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
        rss_text = rss_feed.text
        soup = BeautifulSoup(rss_text, 'xml')
        items = soup.findAll('item')

        data = {
            "data": [
            {
                "title": item.title.text,
                "source": item.source.text,
                "timestamp": datetime.now().timestamp()
            }
            for item in items
            ]
        }
        
        return data

app = Flask(__name__)
conduit = Conduit()

@app.route('/poll', methods=['GET'])
def respond():
    data = conduit.poll()
    return jsonify(data)

if __name__ == '__main__':
    app.run()