"""
Base model with convenience methods for retrieving/writing MongoDB documents.
Requires that a MongoDB url and db be defined in a constants file.
"""
import flask

from pymongo import MongoClient

import constants

def get_db():
  mongo_client = MongoClient(constants.MONGO_URL)
  return mongo_client[constants.DB_NAME]

class BaseModel:
  def __init__(self, **kwargs):
    self._id = kwargs.get('_id')
    self._first_name = kwargs.get('first_name')
    self._last_name = kwargs.get('last_name')
    self._games = kwargs.get('games')
    self._3pm = kwargs.get('3pm')
    self._3pa = kwargs.get('3pa')

  @classmethod
  def get_by_id(cls, id):
    """ Returns an instance of the model from retrieved MongoDB doc. """
    db = get_db()
    collection_name = cls.__name__
    collection = db[collection_name]
    doc = collection.find_one({'_id': id})
    return cls(**doc)

  def put(self):
	db = get_db()
	collection_name = self.__class__.__name__
	collection = db[collection_name]
	collection.update({'_id': self._id}, {"$set": self.__dict__}, 
					  upsert=False)

  def json(self):
    return flask.jsonify(self.__dict__)
	