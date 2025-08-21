# llm.py - Utilities for local LLM inferencing via Foundry Local
# this module is more and more growing to be a robutst but always-simple drop-in LLM library specialized to abstract the complexities and pecularities of Foundry Local.
#
# This module provides functions to interact with locally hosted language models
# using the Foundry Local SDK and OpenAI-compatible API. It can be used to:
#   1 upon module init, discover cached models and load one
#   2 Load and manage local LLMs (e.g., phi-3.5-mini, phi-4)
#   3 Send prompts (such as metadata summaries) to the LLM for recommendations
#   4 Integrate LLM responses into the normalization pipeline
#

# llm.py - Canonical, DRY, atomic, self-initializing LLM interface for Foundry Local


# --- REVIEW: Non-generic and environment-specific imports/config ---
# - Assumes openai and foundry_local are available; not all environments will have these.
# - Imports many config values from .config; these must exist in the new project's config.
# - Uses relative import from .config, which may break if the module is moved or used outside a package.
# - Assumes logging and time are available (these are standard, but still worth noting).
import openai
import logging
import time
from .config import LLM_ENDPOINT, LLM_API_KEY, LLM_ALIAS, LLM_VARIANT, DEFAULT_META_PROMPT, LLM_LOG_PATH, LLM_BACKEND, LLM_LOG_LEVEL, LLM_MAX_TOKENS

_client = None
_model = None
_meta_prompt = None

def _init_llm():
	# --- REVIEW: This function assumes FoundryLocalManager and foundry_local are available if LLM_BACKEND is set accordingly.
	# - If foundry_local is not installed, this will fail unless LLM_BACKEND is set to something else.
	# - The config must provide LLM_ALIAS, LLM_ENDPOINT, LLM_API_KEY, etc. with correct values.
	# - The OpenAI client is initialized with base_url and api_key, which may not be compatible with all OpenAI-like APIs.
	"""
	Initialize the LLM client and model using canonical config values.
	Only runs once per process. Meta prompt is set to the default from config.
	"""
	global _client, _model, _meta_prompt
	if _client is not None and _model is not None and _meta_prompt is not None:
		return
	if LLM_BACKEND.strip().lower() == "foundrylocalmanager":
		try:
			from foundry_local import FoundryLocalManager
		except ImportError:
			# --- REVIEW: This will break if foundry_local is not installed. Consider fallback or clearer error for portability.
			raise ImportError("foundry_local package is required for FoundryLocalManager backend.")
		manager = FoundryLocalManager(LLM_ALIAS)
		_client = openai.OpenAI(base_url=manager.endpoint, api_key=manager.api_key)
		_model = manager.get_model_info(LLM_ALIAS).id
		_meta_prompt = DEFAULT_META_PROMPT
	else:
		_client = openai.OpenAI(base_url=LLM_ENDPOINT, api_key=LLM_API_KEY)
		_model = f"{LLM_ALIAS}-{LLM_VARIANT}"
		_meta_prompt = DEFAULT_META_PROMPT

def set_meta_prompt(prompt):
	"""
	Set the meta/system prompt for LLM chat. This updates the internal state.
	"""
	global _meta_prompt
	_meta_prompt = prompt

def llm_complete(messages, system_prompt=None, **kwargs):
	# --- REVIEW: This function assumes a specific OpenAI-compatible API and config structure.
	# - Uses LLM_LOG_PATH for logging; this must be writable and exist in config.
	# - Uses LLM_MAX_TOKENS, LLM_LOG_LEVEL, etc. from config; these must be defined.
	# - Uses OpenAI's chat.completions.create method, which may not be available in all OpenAI-like clients.
	# - Assumes messages is a list of dicts in OpenAI format.
	# - Uses system prompt logic that may not be compatible with all LLM APIs.
	# - Uses file-based logging, which may not be portable to all environments (e.g., serverless, cloud).
	"""
	Stateless LLM completion: sends a single message list (OpenAI-style) and returns the response.
	Prepends the meta/system prompt if set, or uses the provided system_prompt for this call only.
	Logs LLM-transaction-relevant details: endpoint, model, payload/message count, payload size, timing, and response size.
	Args:
		messages: List of dicts, e.g. [{"role": "user", "content": "..."}]
		system_prompt: Optional string to use as the system/meta prompt for this call only.
		kwargs: Additional OpenAI chat params (e.g., temperature)
	Returns:
		The LLM's response message (str)
	"""
	_init_llm()
	msgs = messages[:]
	prompt_to_use = system_prompt if system_prompt is not None else _meta_prompt
	if prompt_to_use:
		msgs = [{"role": "system", "content": prompt_to_use}] + msgs
	payload_len = sum(len(m.get('content', '')) for m in msgs)
	payload_count = len(msgs)
	# Always pass max_tokens from config to the OpenAI API call, do not inject into kwargs
	# Step-by-step, readable logging for all major steps (all levels), and JSONL payloads at DEBUG
	import os
	# --- REVIEW: This will fail if LLM_LOG_PATH is not set or is not a valid path.
	# - os.makedirs may fail if the directory is not writable or does not exist.
	os.makedirs(os.path.dirname(LLM_LOG_PATH), exist_ok=True)
	def log_to_file(msg):
		try:
			with open(LLM_LOG_PATH, 'a', encoding='utf-8') as f:
				f.write(msg + '\n')
		except Exception as e:
			logging.error(f"Failed to write LLM log to {LLM_LOG_PATH}: {e}")

	# 1. Prompt preparation
	# --- REVIEW: Logging and prompt handling are tightly coupled to config and file system.
	prep_msg = (
		f"\n[LLM STEP 1: Prompt Preparation]"
		f"\nSystem prompt: {prompt_to_use}"
		f"\nUser prompt: {messages[-1]['content'] if messages else ''}"
		f"\n---"
	)
	logging.debug(prep_msg)
	log_to_file(prep_msg)

	# 2. Payload construction
	# --- REVIEW: Assumes LLM_ENDPOINT, _model, and LLM_MAX_TOKENS are always set and valid.
	payload_msg = (
		f"[LLM STEP 2: Payload Construction]"
		f"\nEndpoint: {LLM_ENDPOINT}"
		f"\nModel: {_model}"
		f"\nMessage count: {payload_count}"
		f"\nPayload chars: {payload_len}"
		f"\nmax_tokens: {LLM_MAX_TOKENS}"
		f"\nPayload kwargs: {kwargs}"
		f"\n---"
	)
	logging.debug(payload_msg)
	log_to_file(payload_msg)

	# 3. Sending request
	# --- REVIEW: Assumes _client is a valid OpenAI client and will not fail on .chat.completions.create.
	send_msg = (
		f"[LLM STEP 3: Sending Request]"
		f"\nSending request to LLM..."
		f"\n---"
	)
	logging.debug(send_msg)
	log_to_file(send_msg)

	# DEBUG: log full request payload as single-line JSONL
	# --- REVIEW: Uses json and logs full payloads; may expose sensitive data if not careful.
	if LLM_LOG_LEVEL.strip().upper() == "DEBUG":
		import json
		request_payload = {
			'endpoint': LLM_ENDPOINT,
			'model': _model,
			'messages': msgs,
			'max_tokens': LLM_MAX_TOKENS,
			'kwargs': kwargs
		}
		log_to_file('[LLM DEBUG] REQUEST PAYLOAD: ' + json.dumps(request_payload, ensure_ascii=False))

	start_time = time.time()
	try:
		response = _client.chat.completions.create(
			model=_model,
			messages=msgs,
			max_tokens=LLM_MAX_TOKENS,
			**kwargs
		)
		elapsed = time.time() - start_time
		resp_content = response.choices[0].message.content
		resp_len = len(resp_content) if resp_content else 0

		# 4. Response received
		resp_msg = (
			f"[LLM STEP 4: Response Received]"
			f"\nElapsed: {elapsed:.2f}s"
			f"\nResponse chars: {resp_len}"
			f"\nResponse:\n{resp_content}"
			f"\n{'='*40}"
		)
		logging.debug(resp_msg)
		log_to_file(resp_msg)

		# DEBUG: log full response payload as single-line JSONL
		if LLM_LOG_LEVEL.strip().upper() == "DEBUG":
			import json
			response_payload = {
				'elapsed': elapsed,
				'response_chars': resp_len,
				'response': resp_content
			}
			log_to_file('[LLM DEBUG] RESPONSE PAYLOAD: ' + json.dumps(response_payload, ensure_ascii=False))

		if LLM_LOG_LEVEL.strip().upper() != "DEBUG":
			logging.info("[LLM] Request sent: endpoint=%s, model=%s, message_count=%d, payload_chars=%d", LLM_ENDPOINT, _model, payload_count, payload_len)
			logging.info("[LLM] Response received: elapsed=%.2fs, response_chars=%d", elapsed, resp_len)
		return resp_content
	except Exception as e:
		err_msg = (
			f"[LLM STEP 5: ERROR]"
			f"\nException occurred during LLM request: {e}"
			f"\n{'='*40}"
		)
		logging.error(err_msg)
		log_to_file(err_msg)
		raise

# --- SUMMARY OF NON-GENERIC/INCOMPATIBLE ASPECTS ---
# 1. Assumes a specific config structure and presence of many LLM-related config values.
# 2. Assumes OpenAI and optionally foundry_local are installed and available.
# 3. Uses relative import from .config, which may break if moved or used as a standalone script.
# 4. Uses file-based logging and expects LLM_LOG_PATH to be valid and writable.
# 5. Assumes OpenAI-compatible API for all LLM operations (may not work with other LLM APIs).
# 6. Hardcodes some prompt and model logic (e.g., f"{LLM_ALIAS}-{LLM_VARIANT}") that may not generalize.
# 7. Not all environments will have the same directory structure or config management.
# 8. Error handling and logging are tightly coupled to the config and file system.
#
# RECOMMENDATIONS:
# - Refactor to allow injection of config and logging dependencies.
# - Support environment variable fallback or config autodiscovery.
# - Allow for pluggable LLM backends, not just OpenAI/foundry_local.
# - Avoid relative imports for better portability.
# - Make logging optional or allow for in-memory/stream logging.
# - Document all required config values and expected environment structure.
