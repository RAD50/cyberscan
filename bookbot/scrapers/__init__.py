"""Scrapers module for searching bookstore websites."""

from .base_scraper import BaseScraper
from .hiber_scraper import HiberScraper
from .thawaqa_scraper import ThawaqaScraper
from .rawazin_scraper import RawazinScraper
from .ain_scraper import AinScraper

__all__ = [
    "BaseScraper",
    "HiberScraper",
    "ThawaqaScraper",
    "RawazinScraper",
    "AinScraper",
]
