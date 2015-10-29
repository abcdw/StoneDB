# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request, Response
from functools import wraps
from database import DBMS

# import some db stuff
import json

app = Flask(__name__)


@app.route("/")
def hello(name=None):
    # render static
    # print 'ok'
    return render_template('table.html', name=name)
    return "Hello World!"




@app.route("/articles")
@app.route("/articles/<q>")
def get_articles(range=None):
    # return json response
    #  articles = range(0, 10)
    #  print 'ok'
    q = 'test'
    # print 'ok'
    db = DBMS('stoneDB', 'postgres', 'postgres', 'localhost')
    query = request.args.get('q', 'test')
    rows = db.search_by_title(query)
    result = []
    for row in rows:
        rrow = {'id': row[0],
                'title': row[1],
                'year': row[2],
                # 'venue_id': row[3]
                }
        result.append(rrow)
    return json.dumps(result)


@app.route("/create_article", methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        print request.data
        print 'ok'
        # get some values from request.form
        return 'Your article was added'
        # do some magic stuff
    if request.method == 'GET':
        return render_template('create_article.html')

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'admin'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/article")
@requires_auth
def get_article():
    return "Article"


if __name__ == "__main__":
    app.run()
