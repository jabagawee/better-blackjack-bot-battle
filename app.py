#! /usr/bin/env python

import datetime
import os
import random
from functools import wraps

import pymongo
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

connection = pymongo.Connection(host=os.environ['MONGOLAB_URI'])
db = connection[os.environ['MONGOLAB_DATABASE']]
auth_collection = db['auth']

app = Flask(__name__)


@app.route('/')
def root():
    username = None
    if 'apikey' in request.args:
        apikey = request.args['apikey']
        document = auth_collection.find_one({'apikey': apikey})
        if document:
            username = document['username']
            in_game = document['in_game']
            cash = document['cash']
    if username is None:
        username = "Anonymous"
        in_game = False
        cash = 0
    if in_game:
        return "Hello, %s. \
                You are currently in a game and you have $%d." \
                % (username, cash)
    return "Hello, %s. \
            You are currently not in a game and you have $%d." \
            % (username, cash)


def generate_apikey():
    valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(valid_chars) for __ in xrange(25))


@app.route('/api/keys/get')
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
                'created_time': datetime.datetime.utcnow(),
                'cash': 5000,
                'in_game': False}
    auth_collection.insert(document)
    return jsonify({'success': True, 'apikey': apikey})


def valid_apikey_required(view):
    @wraps(view)
    def decorated_view(*args, **kwargs):
        if 'apikey' not in request.args:
            return jsonify({'success': False, 'error': 'No apikey found.'})
        apikey = request.args['apikey']
        document = auth_collection.find_one({'apikey', apikey})
        if document:
            return view(*args, **kwargs)
        return jsonify({'success': False, 'error': 'Invalid apikey.'})
    return decorated_view


@app.route('/api/keys/check')
@valid_apikey_required
def check_apikey():
    document = auth_collection.find_one({'apikey', request.args['apikey']})
    return jsonify({'success': True,
                    'username': document['username'],
                    'cash': document['cash'],
                    'in_game': document['in_game']})


@app.route('/api/game/new')
@valid_apikey_required
def new_game():
    pass


@app.route('/api/game/hit')
@valid_apikey_required
def hit():
    pass


@app.route('/api/game/stand')
@valid_apikey_required
def stand():
    pass


@app.route('/api/game/double_down')
@valid_apikey_required
def double_down():
    pass


@app.route('/api/game/surrender')
@valid_apikey_required
def surrender():
    pass


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
