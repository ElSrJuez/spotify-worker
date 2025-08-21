
"""
Spotify Worker: Interacts with the Spotify Web API to create/edit playlists based on web searches and AI prompts.
"""

from src import config, db

class SpotifyWorker:
	def __init__(self):
		self.client_id = config.SPOTIFY_CLIENT_ID
		self.client_secret = config.SPOTIFY_CLIENT_SECRET
		self.redirect_uri = config.SPOTIFY_REDIRECT_URI
		self.db = db.db

	def create_playlist(self, user_id, name, description=""):
		# TODO: Implement playlist creation using Spotify API
		pass

	def edit_playlist(self, playlist_id, tracks):
		# TODO: Implement playlist editing using Spotify API
		pass

	def search_tracks(self, query):
		# TODO: Implement track search using Spotify API
		pass

	def save_to_db(self, data):
		# Example: Save data to TinyDB
		self.db.insert(data)

# Dev Principles
# - Separation of Concerns
# - DRY
# - Keep Files Short and Sweet
# - No secret nor populated configuration files committed to Git


