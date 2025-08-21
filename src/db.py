from tinydb import TinyDB, Query
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'spotify_db.json')
db = TinyDB(db_path)
