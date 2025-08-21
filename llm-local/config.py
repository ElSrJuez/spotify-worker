
# Private config utility for llm-local
# Loads config from config.ini in the same directory.
# Provides validation and clear error messages for missing values.

import configparser
import os

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
_config = configparser.ConfigParser()
if not os.path.exists(_CONFIG_PATH):
	raise FileNotFoundError(f"llm-local/config.ini not found. Please copy config.ini.example and fill in the required values.")
_config.read(_CONFIG_PATH)

def _get(section, key, required=True, fallback=None):
	if _config.has_option(section, key):
		return _config.get(section, key)
	if required:
		raise ValueError(f"Missing required config value: [{section}] {key}")
	return fallback

LLM_ENDPOINT = _get('llm', 'endpoint')
LLM_API_KEY = _get('llm', 'api_key')
LLM_ALIAS = _get('llm', 'alias')
LLM_VARIANT = _get('llm', 'variant')
DEFAULT_META_PROMPT = _get('llm', 'default_meta_prompt')
LLM_LOG_PATH = _get('llm', 'llm_log')
LLM_BACKEND = _get('llm', 'llm_backend')
LLM_LOG_LEVEL = _get('llm', 'log_level')
LLM_MAX_TOKENS = int(_get('llm', 'max_tokens'))
