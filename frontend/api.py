import datetime
import json
from flask import request, abort
from flask.ext import restful
from flask.ext.restful import reqparse
from pymongo import MongoClient

import constants
from lib.pba_client import PBAClient
from models import *
from rest_service import app, api


class PlayerHandler(restful.Resource):
  def get(self, player_name):
	  # Get our local copy of the player.
	  player = Player.get_by_id(player_name)
	
	  # Get updated data from the remote service.
	  first_name, last_name = player_name.split('_')
	  pba_client = PBAClient()
	  pba_client.search_player(first_name, last_name)
	
	  return player.json()

  def post(self):
	  params = request.get_json()
	  _id = params.get('_id')
	  player = Player.get_by_id(_id)
	  player.update_stats(params)


api.add_resource(PlayerHandler, 
			     '/api/player/<string:player_name>', 
				   '/api/player/')