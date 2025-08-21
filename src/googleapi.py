# Google Search API utility
import requests
import logging
from src.config import GOOGLE_SEARCH_API_KEY, GOOGLE_CSE_ID

class GoogleSearch:
	def __init__(self, api_key=None, cse_id=None):
		self.api_key = api_key or GOOGLE_SEARCH_API_KEY
		self.cse_id = cse_id or GOOGLE_CSE_ID
		logging.info(f"[GoogleSearch] Initialized with API key set: {bool(self.api_key)}, CSE ID set: {bool(self.cse_id)}")

	def search(self, query, num=5):
		"""
		Send a prompt to Google Custom Search API and return results.
		"""
		if not self.api_key or not self.cse_id:
			logging.error("[GoogleSearch] Google API key and CSE ID must be set.")
			raise ValueError("Google API key and CSE ID must be set.")
		url = "https://www.googleapis.com/customsearch/v1"
		params = {
			'key': self.api_key,
			'cx': self.cse_id,
			'q': query,
			'num': num
		}
		logging.info(f"[GoogleSearch] Query: '{query}', Params: {params}")
		try:
			resp = requests.get(url, params=params)
			resp.raise_for_status()
			items = resp.json().get('items', [])
			logging.info(f"[GoogleSearch] Got {len(items)} results for query '{query}'")
			return items
		except Exception as e:
			logging.error(f"[GoogleSearch] Error during search: {e}")
			raise
# this is a self-initializing, self contained helper module for interacting with the Google Search API
