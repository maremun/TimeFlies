#	encoding: utf8
#	app.py

from flask import Flask, jsonify, current_app, request


app = Flask(__name__)


@app.route('/webhook/', methods=['POST'])
def index():
    name = request.json['name']
    return jsonify(msg='hello, %s' % name), 200
