# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
# import some db stuff
import json

app = Flask(__name__)

@app.route("/")
def hello(name=None):
    # render static
    return render_template('index.html', name=name)
    return "Hello World!"


@app.route("/articles")
@app.route("/articles/<range>")
def get_articles(range=None):
    # return json response
    articles = range(0, 10)
    return json.dumps(articles)


@app.route("/article")
def get_article():
    return "Article"


if __name__ == "__main__":
    app.run()
