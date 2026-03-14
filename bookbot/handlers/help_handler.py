"""
Handler for /help command.
Shows usage instructions in the user's selected language.
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from ..security import restricted
from ..translations import get_message
from ..user_data import get_language

logger = logging.getLogger(__name__)


@restricted
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command — show usage instructions."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    await update.message.reply_text(get_message("help_text", lang))
    logger.info("User %s requested help.", update.effective_user.id)
