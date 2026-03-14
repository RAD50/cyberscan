"""
Omani Book Bot — Main entry point.
A Telegram bot that searches for books across 4 Omani bookstore websites
and presents results in a bilingual (AR/EN) interface.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Ensure the parent directory of bookbot/ is on sys.path so that
# 'bookbot' can be imported as a package with relative imports.
_script_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_script_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

# Load environment variables from .env file (look in the script's directory)
load_dotenv(os.path.join(_script_dir, ".env"))


def setup_logging() -> None:
    """
    Configure logging with rotating file handlers and console output.
    Creates the logs/ directory if it doesn't exist.
    """
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    root_logger.addHandler(console_handler)

    # General bot log — rotating file handler (max 5MB, 3 backups)
    bot_log_path = os.path.join(log_dir, "bot.log")
    bot_file_handler = RotatingFileHandler(
        bot_log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    bot_file_handler.setLevel(getattr(logging, log_level, logging.INFO))
    bot_file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    root_logger.addHandler(bot_file_handler)

    # Unauthorized access log — rotating file handler (max 2MB, 2 backups)
    log_unauthorized = os.environ.get("LOG_UNAUTHORIZED", "true").lower() == "true"
    if log_unauthorized:
        unauth_log_path = os.path.join(log_dir, "unauthorized.log")
        unauth_handler = RotatingFileHandler(
            unauth_log_path, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
        )
        unauth_handler.setLevel(logging.WARNING)
        unauth_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        unauth_logger = logging.getLogger("unauthorized")
        unauth_logger.addHandler(unauth_handler)
        unauth_logger.propagate = False  # Don't duplicate to root logger


def main() -> None:
    """Initialize and run the Telegram bot."""
    setup_logging()
    logger = logging.getLogger(__name__)

    # Validate bot token
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        logger.critical("TELEGRAM_BOT_TOKEN is not set. Exiting.")
        sys.exit(1)

    logger.info("Starting Omani Book Bot...")

    # Import handlers after logging is configured
    from bookbot.handlers.start_handler import start_command, language_callback
    from bookbot.handlers.help_handler import help_command
    from bookbot.handlers.search_handler import (
        search_command,
        text_search_handler,
        search_again_callback,
    )
    from bookbot.handlers.language_handler import language_command
    from bookbot.handlers.admin_handler import (
        whitelist_command,
        adduser_command,
        removeuser_command,
        status_command,
    )

    # Build the application
    application = ApplicationBuilder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("language", language_command))

    # Admin commands
    application.add_handler(CommandHandler("whitelist", whitelist_command))
    application.add_handler(CommandHandler("adduser", adduser_command))
    application.add_handler(CommandHandler("removeuser", removeuser_command))
    application.add_handler(CommandHandler("status", status_command))

    # Callback query handlers for inline buttons
    application.add_handler(
        CallbackQueryHandler(language_callback, pattern="^lang_(en|ar)$")
    )
    application.add_handler(
        CallbackQueryHandler(search_again_callback, pattern="^search_again$")
    )

    # Plain text message handler (must be last to catch all non-command text)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_search_handler)
    )

    # Start the bot with polling
    logger.info("Bot is running. Polling for updates...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
