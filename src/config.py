

import configparser
import os

# Canonical config.ini path (project root)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Spotify API credentials
SPOTIFY_CLIENT_ID = config.get('spotify', 'client_id', fallback=None)
SPOTIFY_CLIENT_SECRET = config.get('spotify', 'client_secret', fallback=None)
SPOTIFY_REDIRECT_URI = config.get('spotify', 'redirect_uri', fallback=None)
SPOTIFY_SCOPE = config.get('spotify', 'scope', fallback='playlist-modify-public playlist-modify-private playlist-read-private user-read-private')
SPOTIFY_TOKEN_CACHE = config.get('spotify', 'token_cache', fallback='.spotify_token_cache')
