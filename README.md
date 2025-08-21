
# spotify-worker

## Project Objective
spotify-worker is a modular Python utility designed to interact with the Spotify Web API for the purpose of creating, editing, and managing playlists based on web searches and AI prompts. It provides a clean, configurable, and extensible foundation for automating playlist management and related Spotify tasks.

## Project Principles
- **Separation of Concerns:** Each module and component has a single, well-defined responsibility.
- **DRY (Don't Repeat Yourself):** Code and configuration are structured to avoid unnecessary duplication.
- **Keep Files Short and Sweet:** Source files are concise and focused for maintainability.
- **No Secrets in Git:** No secret or populated configuration files are committed to version control. All sensitive data is managed via a canonical, gitignored `config.ini` file, with a tracked `config.ini.example` for reference.
- **Consistent Configuration:** All runtime parameters are managed through a single, canonical configuration file.

## Description
spotify-worker provides a self-contained worker and utility modules for interacting with the Spotify Web API. It supports:
- Secure, centralized configuration using a canonical `config.ini` file.
- Playlist creation, editing, and track search via the Spotify API.
- Extensible architecture for integrating AI-driven playlist suggestions and web search features.
- Data persistence using TinyDB for lightweight, file-based storage.
- Clear separation between configuration, data, and code, following best practices for maintainability and security.

This project is suitable for developers seeking a robust foundation for Spotify automation, playlist curation, or integration with AI and web-based music discovery tools.
