

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

def print_menu():
	print("\nSpotify Playlist Worker")
	print("1. List my playlists")
	print("2. Create a new playlist")
	print("3. Add tracks to a playlist")
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
			name = input("Playlist name: ").strip()
			desc = input("Description (optional): ").strip()
			playlist = api.create_playlist(user_id, name, description=desc)
			print(f"Created playlist: {playlist['name']} (ID: {playlist['id']})")

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


