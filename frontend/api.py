import datetime
import json
from flask import request, abort
from flask.ext import restful
from flask.ext.restful import reqparse
from pymongo import MongoClient

import constants
from rest_service import app, api
from models import *


class PlayerHandler(restful.Resource):
  def get(self, player_name):
	player = Player.get_by_id(player_name)
	return player.json()

  def post(self):
	params = request.get_json()
	_id = params.get('_id')
	player = Player.get_by_id(_id)
	player.put()


api.add_resource(PlayerHandler, 
			     '/api/player/<string:player_name>', 
				 '/api/player/')