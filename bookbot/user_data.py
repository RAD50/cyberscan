"""
In-memory user language preferences per chat_id.
Optionally persists to a local JSON file so preferences survive restarts.
"""

import json
import logging
import os

logger = logging.getLogger(__name__)

# In-memory store: {chat_id (int): language_code (str)}
_user_languages: dict[int, str] = {}

# Path to the persistent JSON file
_DATA_FILE = os.path.join(os.path.dirname(__file__), "user_languages.json")

# Default language
DEFAULT_LANGUAGE = "en"


def _load_from_file() -> None:
    """Load user language preferences from the JSON file on disk."""
    global _user_languages
    if os.path.exists(_DATA_FILE):
        try:
            with open(_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert string keys back to int (JSON keys are always strings)
                _user_languages = {int(k): v for k, v in data.items()}
                logger.info("Loaded %d user language preferences from disk.", len(_user_languages))
        except (json.JSONDecodeError, ValueError, OSError) as e:
            logger.warning("Failed to load user data from %s: %s", _DATA_FILE, e)
            _user_languages = {}


def _save_to_file() -> None:
    """Persist user language preferences to the JSON file on disk."""
    try:
        with open(_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_languages, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.warning("Failed to save user data to %s: %s", _DATA_FILE, e)


def get_language(chat_id: int) -> str:
    """Get the language preference for a given chat_id."""
    return _user_languages.get(chat_id, DEFAULT_LANGUAGE)


def set_language(chat_id: int, language: str) -> None:
    """Set the language preference for a given chat_id and persist to disk."""
    _user_languages[chat_id] = language
    _save_to_file()


# Load preferences from disk on module import
_load_from_file()
