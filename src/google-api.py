# Google Search API utility
import requests
from src.config import GOOGLE_SEARCH_API_KEY

class GoogleSearch:
	def __init__(self, api_key=None, cse_id=None):
		self.api_key = api_key or GOOGLE_SEARCH_API_KEY
		# You may want to add CSE ID to config and pass here as well
		self.cse_id = cse_id

	def search(self, query, num=5):
		"""
		Send a prompt to Google Custom Search API and return results.
		"""
		if not self.api_key or not self.cse_id:
			raise ValueError("Google API key and CSE ID must be set.")
		url = "https://www.googleapis.com/customsearch/v1"
		params = {
			'key': self.api_key,
			'cx': self.cse_id,
			'q': query,
			'num': num
		}
		resp = requests.get(url, params=params)
		resp.raise_for_status()
		return resp.json().get('items', [])
# this is a self-initializing, self contained helper module for interacting with the Google Search API
