# Moody Playlist Utility: Minimal, DRY, and Principle-Aligned Skeleton

## File: util/moody-playlist.py

### Public Interface
- `create_moody_playlist(mood_prompt, thoughts_file=None)`
	- Accepts only the mood prompt and optional thoughts file.
	- Handles all context gathering, normalization, and playlist creation internally.
	- Does NOT require user_id, cse_id, or any Spotify details from the caller.
	- Returns a summary/result object (playlist name, etc).

### Private Helpers (internal use only)
- `_read_and_normalize_thoughts(thoughts_file)`
- `_shorten_google_results(results)`
- (other normalization/context helpers as needed)

## Principles
- No user_id or Spotify details in the public interface—handled internally by the Spotify utility.
- Tracks and songs are managed by their respective utilities, not mixed in the playlist orchestration.
- No “add moody song” in this context—focus is only on the playlist creation workflow (steps 1–3.1).
- No unnecessary parameters (like cse_id) exposed to the CLI or user.

---
# Moody Playlist Utility: Structural Skeleton (Simplicity & DRY)

## File: util/moody-playlist.py

### Public Interface
- `create_moody_playlist(user_id, mood_prompt, thoughts_file=None, cse_id=None)`  
	- Orchestrates all context gathering, normalization, and playlist creation.  
	- Returns a summary/result object (playlist name, tracks, etc).

- `add_moody_song_to_playlist(user_id, playlist_id, mood_prompt, thoughts_file=None, cse_id=None)`  
	- Adds a single LLM/Google/thoughts-driven song to an existing playlist.

### Private Helpers
- `_read_and_normalize_thoughts(thoughts_file)`
- `_shorten_google_results(results)`
- (other normalization/context helpers as needed)

## File: playlist-worker.py (CLI)

- Only gathers user input (mood prompt, optional thoughts file, playlist id if needed).
- Calls the above public interface functions.
- Displays results.

---

**Principles:**
- All orchestration and logic is in the utility module, not the CLI.
- CLI is minimal, DRY, and only responsible for user interaction.
- Utility module is the single source of truth for the workflow.

# Moody Playlist Utility: Design & Decisions Summary (as of Aug 2025)

## Agreed-Upon Actions & Principles

- **Separation of Concerns:**
	- All API and orchestration logic is in utility modules, not in the main CLI.
	- The main app only gathers user input and calls utility functions.

- **Utility Functions:**
	- `create_moody_playlist`: Orchestrates the full workflow for creating a moody playlist (Google search, LLM, song proposals, playlist creation).
	- `add_moody_song_to_playlist`: Adds a single moody song to any playlist using the same context pipeline.

- **Persistence (TinyDB):**
	- Only the minimal "moody playlist song proposals object" (generated song queries, context, and prompt) will be persisted.
	- No playlist IDs or user history will be stored, to avoid complexity and scope creep.
	- Persistence is optional and for possible inspection or reuse, not for full re-creation or analytics.

- **Scope Management:**
	- Avoiding unnecessary features and complexity.
	- Focus is on core functionality and maintainability.

---

This summary reflects the current design and priorities for the moody playlist utility. Any future changes should revisit these principles to avoid scope creep.
