"""
Handler for /language command.
Allows the user to change their language preference at any time.
"""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..security import restricted
from ..translations import get_message
from ..user_data import get_language

logger = logging.getLogger(__name__)


@restricted
async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /language command — show language selection buttons."""
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
        get_message("choose_language", lang),
        reply_markup=reply_markup,
    )
    logger.info("User %s requested language change.", update.effective_user.id)
