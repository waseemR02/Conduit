from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime


class Conduit:
    def __init__(self):
        self.conn = sqlite3.connect('/home/news.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS news (title TEXT, source Text, time INTEGER(11))')
        self.conn.commit()


    def write_to_db(self, data: list):
        c = self.conn.cursor()
        c.executemany('INSERT INTO news VALUES (?,?,?)', data)
        self.conn.commit()

    def poll(self):
        rss_feed = requests.get("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
        rss_text = rss_feed.text
        soup = BeautifulSoup(rss_text, 'xml')
        items = soup.findAll('item')

        data = [(item.title.text, item.source.text, datetime.now().timestamp()) for item in items]
        
        self.write_to_db(data)


if __name__ == '__main__':
    conduit = Conduit()
    conduit.poll()