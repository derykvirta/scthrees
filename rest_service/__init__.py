import os
import jinja2

from flask import Flask
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps

import constants

MONGO_URL = constants.MONGO_URL

app = Flask(__name__, static_url_path='')

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('templates/'),
])

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

from frontend import views
from frontend import api