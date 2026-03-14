"""
Access control module for the Telegram Book Bot.
Provides whitelist-based access control with @restricted and @admin_only decorators.
"""

import functools
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
unauth_logger = logging.getLogger("unauthorized")


def _get_allowed_user_ids() -> list[int]:
    """
    Load ALLOWED_USER_IDS from environment at runtime (supports hot-reload).
    Returns an empty list if not set or empty (open mode).
    """
    raw = os.environ.get("ALLOWED_USER_IDS", "").strip()
    if not raw:
        return []
    try:
        return [int(uid.strip()) for uid in raw.split(",") if uid.strip()]
    except ValueError:
        logger.warning("Invalid ALLOWED_USER_IDS format: %s", raw)
        return []


def _get_admin_user_ids() -> list[int]:
    """
    Load ADMIN_USER_IDS from environment at runtime.
    Returns an empty list if not set or empty.
    """
    raw = os.environ.get("ADMIN_USER_IDS", "").strip()
    if not raw:
        return []
    try:
        return [int(uid.strip()) for uid in raw.split(",") if uid.strip()]
    except ValueError:
        logger.warning("Invalid ADMIN_USER_IDS format: %s", raw)
        return []


def _log_unauthorized_access(update) -> None:
    """Log an unauthorized access attempt with full details."""
    user = update.effective_user
    chat = update.effective_chat

    log_unauthorized = os.environ.get("LOG_UNAUTHORIZED", "true").lower() == "true"
    if not log_unauthorized:
        return

    user_id = user.id if user else "N/A"
    username = f"@{user.username}" if user and user.username else "N/A"
    first_name = user.first_name if user and user.first_name else "N/A"
    last_name = user.last_name if user and user.last_name else "N/A"
    chat_id = chat.id if chat else "N/A"
    message_text = update.message.text if update.message else "N/A"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    log_msg = (
        f"UNAUTHORIZED ACCESS | "
        f"Time: {timestamp} | "
        f"User ID: {user_id} | "
        f"Username: {username} | "
        f"Name: {first_name} {last_name} | "
        f"Chat ID: {chat_id} | "
        f"Message: {message_text}"
    )

    unauth_logger.warning(log_msg)
    logger.warning(log_msg)


def is_user_allowed(user_id: int) -> bool:
    """Check if a user ID is allowed to use the bot."""
    allowed = _get_allowed_user_ids()
    # If whitelist is empty, all users are allowed (open mode)
    if not allowed:
        return True
    return user_id in allowed


def is_user_admin(user_id: int) -> bool:
    """Check if a user ID has admin privileges."""
    admins = _get_admin_user_ids()
    return user_id in admins


def restricted(func):
    """
    Decorator that restricts handler access to whitelisted users only.
    Unauthorized users are silently ignored (no reply, no error message).
    """
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        if not user:
            return

        if not is_user_allowed(user.id):
            _log_unauthorized_access(update)
            return

        return await func(update, context, *args, **kwargs)

    return wrapper


def admin_only(func):
    """
    Decorator that restricts handler access to admin users only.
    Non-admins are silently ignored.
    """
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        if not user:
            return

        if not is_user_admin(user.id):
            _log_unauthorized_access(update)
            return

        return await func(update, context, *args, **kwargs)

    return wrapper
