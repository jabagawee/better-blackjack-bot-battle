#! /usr/bin/env python

import datetime
import os
import random

import pymongo
from flask import Flask

connection = pymongo.Connection(host=os.environ['MONGOLAB_URI'])
db = connection[os.environ['MONGOLAB_DATABASE']]
auth_collection = db['auth']

app = Flask(__name__)


@app.route('/')
def root():
    return "Hello World"

valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789"


# TODO: change into just /api/register with params username and password
# TODO: turn this into json
@app.route('/api/register/<username>')
def register(username):
    return 'under construction'
    # TODO: add a simple IP address checker to make sure 2 min have passed
    existing_token = auth_collection.find_one({'username': username})
    if existing_token:
        return 'Already registered. Your token is %s.' % (existing_token['token'])
    token = ''.join(random.choice(valid_chars) for __ in xrange(25))
    auth = {'username': username,
            'token': token,
            'created_time': datetime.datetime.utcnow()}
    auth_collection.insert(auth)
    return "Registered. Your token is %s." % (token)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
