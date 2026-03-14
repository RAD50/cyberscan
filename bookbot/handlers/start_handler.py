"""
Handler for /start command.
Shows a welcome message and language selection inline buttons.
"""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..security import restricted
from ..translations import get_message
from ..user_data import get_language, set_language

logger = logging.getLogger(__name__)


@restricted
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command — welcome message with language selection."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_message("welcome", lang),
        reply_markup=reply_markup,
    )
    logger.info("User %s started the bot.", update.effective_user.id)


@restricted
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection from inline buttons."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    if query.data == "lang_en":
        set_language(chat_id, "en")
        await query.edit_message_text(get_message("language_changed", "en"))
    elif query.data == "lang_ar":
        set_language(chat_id, "ar")
        await query.edit_message_text(get_message("language_changed", "ar"))

    logger.info("User %s changed language to %s.", query.from_user.id, query.data)
