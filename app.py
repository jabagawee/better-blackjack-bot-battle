#! /usr/bin/env python

import datetime
import os
import random

import pymongo
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

connection = pymongo.Connection(host=os.environ['MONGOLAB_URI'])
db = connection[os.environ['MONGOLAB_DATABASE']]
auth_collection = db['auth']

app = Flask(__name__)


@app.route('/')
def root():
    return "Hello World"


def generate_apikey():
    valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(valid_chars) for __ in xrange(25))


@app.route('/api/get_apikey')
def get_apikey():
    if 'username' not in request.args or 'password' not in request.args:
        return jsonify({'success': False,
                        'error': 'Missing username or password.'})

    username, password = request.args['username'], request.args['password']

    # check if user was already here
    document = auth_collection.find_one({'username': username})
    if document:
        if check_password_hash(document['pass_hash'], password):
            return jsonify({'success': True, 'apikey': document['apikey']})
        return jsonify({'success': False, 'error': 'Incorrect password.'})

    apikey = generate_apikey()
    document = {'username': username,
                'pass_hash': generate_password_hash(password),
                'apikey': apikey,
                'created_time': datetime.datetime.utcnow()}
    auth_collection.insert(document)
    return jsonify({'success': True, 'apikey': apikey})


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
