from flask import Flask, jsonify
from os import path, mkdir
import click
import logging

app = Flask(__name__)
#app.debug = False
#app.use_reloader = False
#app.threaded = False
#app.processes = 1

RESOURCES_PATH = path.join(path.dirname(app.root_path), "resources")
SERIALISED_FILE_PATH = path.join(RESOURCES_PATH, "tweets.json")

app.config["RESOURCES_PATH"] = RESOURCES_PATH
app.config["SERIALISED_FILE_PATH"] = SERIALISED_FILE_PATH

if not path.exists(RESOURCES_PATH):
    mkdir(RESOURCES_PATH)

""" import after app created to avoid circular dependencies """
from main.scraper import Scraper

scraper = Scraper()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


""" Suppress Flask logging messages to stdout"""

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass


def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass


click.echo = echo
click.secho = secho


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/loadTimeline")
def load_timeline():
    scraper.get_feed()
    return jsonify(message="success"), 200


@app.route("/updateTimeline")
def update_timeline():
    scraper.update_feed()
    return jsonify(message="success"), 200


@app.route("/allTweets")
def fetch_tweets():
    tweets_json = scraper.fetch_tweets()
    return jsonify(tweets=tweets_json), 200


