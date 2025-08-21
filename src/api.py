
"""
Spotify API Utility Module
-------------------------
Self-initializing, self-contained module for all Spotify API interactions.
All configuration is managed via the project config, with no hardcoded values.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import config

class SpotifyAPI:
	def __init__(self):
		self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
			client_id=config.SPOTIFY_CLIENT_ID,
			client_secret=config.SPOTIFY_CLIENT_SECRET,
			redirect_uri=config.SPOTIFY_REDIRECT_URI,
			scope=config.SPOTIFY_SCOPE,
			cache_path=config.SPOTIFY_TOKEN_CACHE
		))

	def create_playlist(self, user_id, name, description=""):
		return self.sp.user_playlist_create(user=user_id, name=name, description=description)

	def add_tracks_to_playlist(self, playlist_id, track_ids):
		return self.sp.playlist_add_items(playlist_id, track_ids)

	def search_tracks(self, query, limit=10):
		results = self.sp.search(q=query, type='track', limit=limit)
		return results['tracks']['items']

	def get_user_playlists(self, user_id):
		return self.sp.user_playlists(user_id)

	# Add more methods as needed for your use case
