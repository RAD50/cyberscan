"""
Handler for book search functionality.
Handles /search command and plain text messages to search across all bookstores.
"""

import asyncio
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..scrapers import HiberScraper, ThawaqaScraper, RawazinScraper, AinScraper
from ..security import restricted
from ..translations import get_message
from ..user_data import get_language

logger = logging.getLogger(__name__)

# Initialize all scrapers
SCRAPERS = [
    HiberScraper(),
    ThawaqaScraper(),
    RawazinScraper(),
    AinScraper(),
]


async def _search_all_stores(query: str) -> dict[str, list[dict]]:
    """
    Search all bookstores concurrently and return results grouped by store.
    Returns a dict: {store_name: [results]} or {store_name: []} if no results/error.
    """
    tasks = []
    for scraper in SCRAPERS:
        tasks.append(_safe_search(scraper, query))

    all_results = await asyncio.gather(*tasks)

    results_by_store = {}
    for scraper, store_results in zip(SCRAPERS, all_results):
        results_by_store[scraper.store_name] = store_results

    return results_by_store


async def _safe_search(scraper, query: str) -> list[dict] | None:
    """
    Safely run a scraper search, catching all exceptions.
    Returns None if the scraper failed entirely (store unavailable),
    or an empty list if no results were found.
    """
    try:
        return await scraper.search(query)
    except Exception as e:
        logger.error(
            "Scraper %s failed for query '%s': %s",
            scraper.store_name, query, e,
            exc_info=True,
        )
        return None


@restricted
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /search <book name> command."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    # Extract the query from the command arguments
    if context.args:
        query = " ".join(context.args)
    else:
        await update.message.reply_text(get_message("enter_book", lang))
        return

    await _perform_search(update, context, query, lang)


@restricted
async def text_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle plain text messages as book searches."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)
    query = update.message.text.strip()

    if not query:
        await update.message.reply_text(get_message("enter_book", lang))
        return

    await _perform_search(update, context, query, lang)


@restricted
async def search_again_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the 'Search Again' inline button callback."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    lang = get_language(chat_id)

    await query.message.reply_text(get_message("search_prompt", lang))


async def _perform_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: str, lang: str
) -> None:
    """Core search logic: search all stores and send results to the user."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    logger.info("User %s searching for: '%s'", user_id, query)

    # Send "searching" status message
    status_msg = await update.message.reply_text(get_message("searching", lang))

    # Search all stores concurrently
    results_by_store = await _search_all_stores(query)

    # Track summary
    summary_lines = []
    has_any_result = False
    all_failed = True

    for store_name, store_results in results_by_store.items():
        if store_results is None:
            # Scraper returned None — store unavailable
            summary_lines.append(f"⚠️ {store_name}: Unavailable")
            await context.bot.send_message(
                chat_id=chat_id,
                text=get_message("store_unavailable", lang, store=store_name),
            )
            continue

        all_failed = False

        if not store_results:
            # No results found on this store
            summary_lines.append(f"❌ {store_name}: Not found")
            await context.bot.send_message(
                chat_id=chat_id,
                text=get_message("not_found", lang, store=store_name),
            )
        else:
            has_any_result = True
            for book in store_results:
                availability = (
                    get_message("available", lang)
                    if book["available"]
                    else get_message("unavailable", lang)
                )

                caption = (
                    f"📚 {book['title']}\n"
                    f"{get_message('price', lang, price=book['price'])}\n"
                    f"{availability}\n"
                    f"🏪 {book['store']}"
                )

                keyboard = [
                    [
                        InlineKeyboardButton(
                            get_message("view_on_store", lang, store=book["store"]),
                            url=book["product_url"],
                        )
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                try:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=book["image_url"],
                        caption=caption,
                        reply_markup=reply_markup,
                    )
                except Exception as e:
                    # If photo fails (e.g., invalid URL), send text message instead
                    logger.warning(
                        "Failed to send photo for %s: %s", book["title"], e
                    )
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=caption,
                        reply_markup=reply_markup,
                    )

            summary_lines.append(
                f"✅ {store_name}: {len(store_results)} result(s)"
            )

    # Handle case where all stores failed
    if all_failed:
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_message("all_stores_failed", lang),
        )
        return

    # Send summary
    if not has_any_result:
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_message("no_results", lang, query=query),
        )
    else:
        summary_text = "\n".join(summary_lines)
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_message("summary", lang, summary=summary_text),
        )

    # Send "Search Again" button
    keyboard = [
        [
            InlineKeyboardButton(
                get_message("search_again", lang),
                callback_data="search_again",
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text=get_message("search_prompt", lang),
        reply_markup=reply_markup,
    )

    logger.info("Search completed for user %s, query: '%s'", user_id, query)
