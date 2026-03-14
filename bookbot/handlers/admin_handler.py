"""
Admin command handlers.
Provides /whitelist, /adduser, /removeuser, and /status commands.
"""

import logging
import os

from telegram import Update
from telegram.ext import ContextTypes

from ..security import restricted, admin_only
from ..security.access_control import _get_allowed_user_ids, _get_admin_user_ids
from ..translations import get_message
from ..user_data import get_language

logger = logging.getLogger(__name__)


@restricted
@admin_only
async def whitelist_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /whitelist — show all whitelisted user IDs."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    allowed = _get_allowed_user_ids()
    if not allowed:
        await update.message.reply_text(get_message("whitelist_empty", lang))
    else:
        user_list = "\n".join(str(uid) for uid in allowed)
        await update.message.reply_text(
            f"{get_message('whitelist_header', lang)}\n{user_list}"
        )

    logger.info("Admin %s viewed whitelist.", update.effective_user.id)


@restricted
@admin_only
async def adduser_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /adduser <user_id> — add a user to the whitelist at runtime."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    if not context.args:
        await update.message.reply_text(get_message("invalid_user_id", lang))
        return

    try:
        new_user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(get_message("invalid_user_id", lang))
        return

    # Get current whitelist and add the new user
    allowed = _get_allowed_user_ids()
    if new_user_id not in allowed:
        allowed.append(new_user_id)
    # Always update the env var to ensure consistency
    os.environ["ALLOWED_USER_IDS"] = ",".join(str(uid) for uid in allowed)

    await update.message.reply_text(
        get_message("user_added", lang, user_id=new_user_id)
    )
    logger.info("Admin %s added user %s to whitelist.", update.effective_user.id, new_user_id)


@restricted
@admin_only
async def removeuser_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /removeuser <user_id> — remove a user from the whitelist at runtime."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    if not context.args:
        await update.message.reply_text(get_message("invalid_user_id", lang))
        return

    try:
        target_user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(get_message("invalid_user_id", lang))
        return

    allowed = _get_allowed_user_ids()
    if target_user_id in allowed:
        allowed.remove(target_user_id)
        os.environ["ALLOWED_USER_IDS"] = ",".join(str(uid) for uid in allowed)
        await update.message.reply_text(
            get_message("user_removed", lang, user_id=target_user_id)
        )
        logger.info(
            "Admin %s removed user %s from whitelist.",
            update.effective_user.id, target_user_id,
        )
    else:
        await update.message.reply_text(
            get_message("user_not_found", lang, user_id=target_user_id)
        )


@restricted
@admin_only
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status — show current bot security mode and user counts."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    allowed = _get_allowed_user_ids()
    admins = _get_admin_user_ids()

    mode = (
        get_message("mode_whitelist", lang)
        if allowed
        else get_message("mode_open", lang)
    )

    status_text = (
        f"{get_message('status_header', lang)}\n"
        f"{get_message('status_mode', lang, mode=mode)}\n"
        f"{get_message('status_whitelist_count', lang, count=len(allowed))}\n"
        f"{get_message('status_admin_count', lang, count=len(admins))}"
    )

    await update.message.reply_text(status_text)
    logger.info("Admin %s checked bot status.", update.effective_user.id)
