#! /usr/bin/env python

import os

import pymongo
from flask import Flask

connection = pymongo.Connection(host=os.environ['MONGOLAB_URI'])
db = connection[os.environ['MONGOLAB_DATABASE']]

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
