"""
Playlist Worker: Menu-based CLI for playlist management.
All actual Spotify API calls are delegated to the SpotifyAPI utility (src/api.py).
No direct Spotify API logic or implementation in this file.
"""

# for Create a Playlist menu item, it asks the user for mood or idea prompt, it offers available thoughts files to optionally add to the context and based on this it:
# (always leveraging util\moody-playlist.py, src\api.py and src\google-api.py respectively)
# 1. creates and then submits a google search prompt object
# 2. the search result is shortened/made efficient for LLM usage
# 2.1 also normalizes for LLM the selected thoughts file
# 3 creates an efficient context combining the user mood prompt, the normalized search results, the selected thoughts file
# 3.1 submits to llm to return a moody, fun, short playlist name
# 4. submits the same context but now to create a Spotify-api-friendly list of proposed Spotify song name searches
# 5 iteratively submits the proposed song names to spotify song search api and returns a song list object
# 6 creates a spotify playlist using the song list object

from src import db
from src.api import SpotifyAPI
from util.moodyplaylist import create_moody_playlist
import os

def print_menu():
	print("\nSpotify Playlist Worker")
	print("1. List my playlists")
	print("2. Create a new Moody playlist")
	print("3. Add Moody tracks to a playlist")
	print("4. Search for tracks")
	print("5. Exit")

def main():
	api = SpotifyAPI()
	user = api.sp.current_user()
	user_id = user['id']

	while True:
		print_menu()
		choice = input("Select an option: ").strip()

		if choice == '1':
			playlists = api.get_user_playlists(user_id)
			print("\nYour Playlists:")
			for idx, pl in enumerate(playlists['items'], 1):
				print(f"{idx}. {pl['name']} (ID: {pl['id']})")

		elif choice == '2':
			print("\n[Moody Playlist Creation]")
			mood_prompt = input("Enter a mood, theme, or idea for your playlist: ").strip()
			# List available thoughts files
			thoughts_dir = os.path.join(os.path.dirname(__file__), 'playlist-thoughts', 'thoughts')
			thoughts_files = [f for f in os.listdir(thoughts_dir) if f.endswith('.md')]
			thoughts_file = None
			if thoughts_files:
				print("Available thoughts files:")
				for idx, fname in enumerate(thoughts_files, 1):
					print(f"  {idx}. {fname}")
				sel = input("Select a thoughts file by number (or press Enter to skip): ").strip()
				if sel.isdigit() and 1 <= int(sel) <= len(thoughts_files):
					thoughts_file = os.path.join(thoughts_dir, thoughts_files[int(sel)-1])
			try:
				result = create_moody_playlist(mood_prompt, thoughts_file)
				print(f"\n[Moody Playlist Created]")
				print(f"Name: {result['playlist_name']}")
				print(f"Tracks added: {result['track_count']}")
				print(f"Playlist ID: {result['playlist_id']}")
			except Exception as e:
				print(f"Error creating moody playlist: {e}")

		elif choice == '3':
			playlist_id = input("Playlist ID: ").strip()
			track_ids = input("Comma-separated Spotify track IDs: ").strip().split(',')
			track_ids = [tid.strip() for tid in track_ids if tid.strip()]
			if not track_ids:
				print("No track IDs provided.")
				continue
			api.add_tracks_to_playlist(playlist_id, track_ids)
			print(f"Added {len(track_ids)} tracks to playlist {playlist_id}.")

		elif choice == '4':
			query = input("Track search query: ").strip()
			results = api.search_tracks(query)
			print("\nSearch Results:")
			for idx, track in enumerate(results, 1):
				artists = ', '.join([a['name'] for a in track['artists']])
				print(f"{idx}. {track['name']} by {artists} (ID: {track['id']})")

		elif choice == '5':
			print("Goodbye!")
			break

		else:
			print("Invalid option. Please try again.")

if __name__ == "__main__":
	main()


