

import configparser
import os

# Canonical config.ini path (project root)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


# Spotify API credentials (no fallbacks, fail if missing)
try:
	SPOTIFY_CLIENT_ID = config.get('spotify', 'client_id')
	SPOTIFY_CLIENT_SECRET = config.get('spotify', 'client_secret')
	SPOTIFY_REDIRECT_URI = config.get('spotify', 'redirect_uri')
	SPOTIFY_SCOPE = config.get('spotify', 'scope')
	SPOTIFY_TOKEN_CACHE = config.get('spotify', 'token_cache')
except Exception as e:
	raise RuntimeError(f"Missing required Spotify config: {e}")


# Logging configuration (no fallbacks, fail if missing)
try:
	LOG_LEVEL = config.get('logging', 'level').upper()
	LOG_FILE = config.get('logging', 'file')
except Exception as e:
	raise RuntimeError(f"Missing required logging config: {e}")

# AI Playlist config (optional, but load if present)
AI_PLAYLIST_PREFIX = config.get('AIPlayList', 'playlist_prefix')


# Google Search API config (no fallbacks, fail if missing)
try:
	GOOGLE_SEARCH_API_KEY = config.get('SearchAPI', 'GoogleSearchAPIKey')
	GOOGLE_CSE_ID = config.get('SearchAPI', 'GoogleCSEID')
except Exception as e:
	raise RuntimeError(f"Missing required Google Search API config: {e}")
