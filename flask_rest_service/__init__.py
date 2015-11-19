import os
from flask import Flask
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps

MONGO_URL = 'mongodb://heroku_nkg65vjs:dm0eagj237ofa7ghgnb63suih2@ds057234.mongolab.com:57234/heroku_nkg65vjs'

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
app.config['MONGOLAB_URI'] = MONGO_URL
mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

import flask_rest_service.resources