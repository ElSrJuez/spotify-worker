"""
Moody Playlist Utility: Minimal, DRY, and Principle-Aligned
----------------------------------------------------------
Exposes a single public function: create_moody_playlist(mood_prompt, thoughts_file=None)
All orchestration, Spotify state, and context gathering are handled internally.
No user_id, cse_id, or Spotify details required from the caller.
"""

from src.api import SpotifyAPI
from src.googleapi import GoogleSearch
from llmlocal import llm

def _read_and_normalize_thoughts(thoughts_file):
    """Read and normalize the selected thoughts file for LLM context."""
    if not thoughts_file:
        return ""
    with open(thoughts_file, 'r', encoding='utf-8') as f:
        return ' '.join(f.read().strip().split())

def _shorten_google_results(results, max_chars=800):
    """Shorten Google search results for LLM context."""
    if not results:
        return ""
    texts = []
    for item in results:
        snippet = item.get('snippet', '')
        title = item.get('title', '')
        texts.append(f"{title}: {snippet}")
    return '\n'.join(texts)[:max_chars]

def create_moody_playlist(mood_prompt, thoughts_file=None):
    """
    Public interface: create a moody playlist from a mood prompt and optional thoughts file.
    Handles all Spotify state, context gathering, and orchestration internally.
    Returns a summary/result object (playlist name, etc).
    """
    print("[MoodyPlaylist] Step 1: Google search for mood/idea...")
    searcher = GoogleSearch()
    google_results = searcher.search(mood_prompt, num=5)
    print(f"[MoodyPlaylist] Google results: {google_results}")
    search_context = _shorten_google_results(google_results)

    print("[MoodyPlaylist] Step 2: Normalize thoughts file...")
    thoughts_context = _read_and_normalize_thoughts(thoughts_file)
    print(f"[MoodyPlaylist] Thoughts context: {thoughts_context}")

    print("[MoodyPlaylist] Step 3: Build LLM context...")
    llm_context = f"Mood prompt: {mood_prompt}\n\nGoogle context: {search_context}\n\nThoughts: {thoughts_context}"
    print(f"[MoodyPlaylist] LLM context:\n{llm_context}")

    print("[MoodyPlaylist] Step 4: Generate playlist name via LLM...")
    playlist_name_prompt = [
        {"role": "user", "content": f"Given the following context, generate a short, fun, moody playlist name.\n\n{llm_context}"}
    ]
    print(f"[MoodyPlaylist] Playlist name LLM prompt: {playlist_name_prompt}")
    playlist_name_response = llm.llm_complete(playlist_name_prompt)
    print(f"[MoodyPlaylist] Playlist name LLM response: {playlist_name_response}")
    playlist_name = playlist_name_response.strip().replace('"', '')

    print("[MoodyPlaylist] Step 5: Generate song search queries via LLM...")
    song_query_prompt = [
        {"role": "user", "content": f"Given the following context, generate a list of 10 Spotify-friendly song search queries (one per line, no numbering, no extra text).\n\n{llm_context}"}
    ]
    print(f"[MoodyPlaylist] Song queries LLM prompt: {song_query_prompt}")
    song_queries_raw = llm.llm_complete(song_query_prompt)
    print(f"[MoodyPlaylist] Song queries LLM response: {song_queries_raw}")
    song_queries = [q.strip() for q in song_queries_raw.split('\n') if q.strip()]

    print("[MoodyPlaylist] Step 6: Search Spotify for tracks and create playlist...")
    api = SpotifyAPI()
    user = api.sp.current_user()
    user_id = user['id']
    found_tracks = []
    for query in song_queries:
        print(f"[MoodyPlaylist] Searching Spotify for: {query}")
        tracks = api.search_tracks(query, limit=1)
        print(f"[MoodyPlaylist] Spotify search result: {tracks}")
        if tracks:
            found_tracks.append(tracks[0]['id'])
    if not found_tracks:
        print("[MoodyPlaylist] No tracks found for generated queries.")
        raise Exception("No tracks found for generated queries.")

    playlist = api.create_playlist(user_id, playlist_name, description=f"Moody playlist: {mood_prompt}")
    print(f"[MoodyPlaylist] Created playlist: {playlist}")
    api.add_tracks_to_playlist(playlist['id'], found_tracks)
    print(f"[MoodyPlaylist] Added tracks: {found_tracks}")

    return {
        'playlist_id': playlist['id'],
        'playlist_name': playlist_name,
        'track_count': len(found_tracks),
        'mood_prompt': mood_prompt,
        'thoughts_file': thoughts_file,
        'google_context': search_context,
        'llm_context': llm_context,
        'llm_playlist_name_prompt': playlist_name_prompt,
        'llm_playlist_name_response': playlist_name_response,
        'llm_song_query_prompt': song_query_prompt,
        'llm_song_query_response': song_queries_raw,
        'spotify_track_ids': found_tracks
    }
