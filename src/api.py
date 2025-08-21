
"""
Spotify API Utility Module
-------------------------
Self-initializing, self-contained module for all Spotify API interactions.
All configuration is managed via the project config, with no hardcoded values.
"""


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import config
import os
import logging

# Setup logging from config
log_kwargs = {'level': getattr(logging, config.LOG_LEVEL, logging.INFO), 'format': '[%(levelname)s] %(message)s'}
if config.LOG_FILE:
	log_kwargs['filename'] = config.LOG_FILE
logging.basicConfig(**log_kwargs)


class SpotifyAPI:
	def __init__(self):
		logging.info(f"Spotify token cache path: {config.SPOTIFY_TOKEN_CACHE}")
		if os.path.exists(config.SPOTIFY_TOKEN_CACHE):
			logging.info("Token cache file exists.")
		else:
			logging.info("Token cache file does NOT exist.")

		self.oauth = SpotifyOAuth(
			client_id=config.SPOTIFY_CLIENT_ID,
			client_secret=config.SPOTIFY_CLIENT_SECRET,
			redirect_uri=config.SPOTIFY_REDIRECT_URI,
			scope=config.SPOTIFY_SCOPE,
			cache_path=config.SPOTIFY_TOKEN_CACHE,
			open_browser=False
		)
		try:
			token_info = self.oauth.get_cached_token()
			if token_info:
				logging.info("Loaded cached Spotify token.")
			else:
				logging.info("No valid cached token found. Starting auth flow.")
				auth_url = self.oauth.get_authorize_url()
				print("\n[Spotify Auth] Please open the following URL in your browser to authorize the app:")
				print(auth_url)
				print("\nAfter authorization, paste the full redirected URL here:")
				response_url = input("Redirected URL: ").strip()
				code = self.oauth.parse_response_code(response_url)
				token_info = self.oauth.get_access_token(code)
			# Spotipy may return a string or a dict depending on version
			if isinstance(token_info, dict):
				access_token = token_info.get('access_token')
			else:
				access_token = token_info
			if not access_token:
				raise Exception("Failed to obtain Spotify access token.")
			self.sp = spotipy.Spotify(auth=access_token)
		except Exception as e:
			logging.error(f"Spotify authentication failed: {e}")
			raise

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
