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


@app.route('/api/register/<username>')
def register(username):
    entry = auth_collection.find_one({'username': username})
    if entry:
        return 'Already registered. Your token is %s' % (entry['token'])
    token = ''.join(random.choice(valid_chars) for __ in xrange(25))
    auth = {'username': username,
            'token': token,
            'created_time': datetime.datetime.utcnow()}
    auth_collection.insert(auth)
    return "Registered. Your token is %s" % (token)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
