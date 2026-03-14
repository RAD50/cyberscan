"""
Abstract base class for all bookstore scrapers.
Each scraper must implement the search() method.
"""

import abc
import logging
import os
from typing import Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Default placeholder image when a book cover is not found
PLACEHOLDER_IMAGE = "https://via.placeholder.com/200x300?text=No+Cover"

# Common headers to avoid being blocked
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
}


class BaseScraper(abc.ABC):
    """Abstract base class for bookstore scrapers."""

    def __init__(self, store_name: str, base_url: str):
        self.store_name = store_name
        self.base_url = base_url
        self.max_retries = 2

        try:
            self.timeout = int(os.environ.get("REQUEST_TIMEOUT", "15"))
        except ValueError:
            logger.warning("Invalid REQUEST_TIMEOUT value, using default 15.")
            self.timeout = 15

        try:
            self.max_results = int(os.environ.get("MAX_RESULTS_PER_SITE", "3"))
        except ValueError:
            logger.warning("Invalid MAX_RESULTS_PER_SITE value, using default 3.")
            self.max_results = 3

    async def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a URL and return a BeautifulSoup object.
        Includes retry logic (max 2 retries) for failed requests.
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self.timeout,
                    headers=DEFAULT_HEADERS,
                    follow_redirects=True,
                ) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    return BeautifulSoup(response.text, "lxml")
            except httpx.TimeoutException:
                logger.warning(
                    "%s: Timeout on attempt %d/%d for URL: %s",
                    self.store_name, attempt, self.max_retries, url,
                )
            except httpx.HTTPStatusError as e:
                logger.warning(
                    "%s: HTTP %d on attempt %d/%d for URL: %s",
                    self.store_name, e.response.status_code, attempt, self.max_retries, url,
                )
            except httpx.RequestError as e:
                logger.warning(
                    "%s: Request error on attempt %d/%d: %s",
                    self.store_name, attempt, self.max_retries, str(e),
                )

        logger.error("%s: All %d attempts failed for URL: %s", self.store_name, self.max_retries, url)
        return None

    @abc.abstractmethod
    async def search(self, query: str) -> list[dict]:
        """
        Search for books matching the query.

        Returns a list of dicts, each with:
            - title (str): Book title
            - price (str): Price with currency, e.g. "5.500 OMR" or "N/A"
            - available (bool): Whether the book is in stock
            - image_url (str): Cover image URL or placeholder
            - product_url (str): Direct link to the product page
            - store (str): Store display name
        """
        pass
