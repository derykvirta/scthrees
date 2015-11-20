import os

# Stats API key and urls.
PBA_API_KEY = 'rjZ8HqAlhTJyndmQ2R1KgU3u4xaWLiBw'
PBA_PLAYER_BASIC = 'http://api.probasketballapi.com/player'

MONGO_URL = os.environ.get('MONGOLAB_URI') or 'mongodb://localhost:27017/test'
DB_NAME = 'nba'