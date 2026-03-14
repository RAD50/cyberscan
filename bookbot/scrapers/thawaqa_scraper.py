"""
Scraper for Thawaqa bookstore (https://thawaqa.com/).
Thawaqa is a WooCommerce-based store; search URL pattern: /?s=QUERY&post_type=product
"""

import logging
from urllib.parse import quote_plus

from .base_scraper import BaseScraper, PLACEHOLDER_IMAGE

logger = logging.getLogger(__name__)


class ThawaqaScraper(BaseScraper):
    """Scraper for Thawaqa bookstore."""

    def __init__(self):
        super().__init__(store_name="Thawaqa", base_url="https://thawaqa.com")

    async def search(self, query: str) -> list[dict]:
        """Search Thawaqa for books matching the query."""
        search_url = f"{self.base_url}/?s={quote_plus(query)}&post_type=product"
        logger.info("%s: Searching for '%s' at %s", self.store_name, query, search_url)

        soup = await self._fetch(search_url)
        if not soup:
            return []

        results = []
        # WooCommerce product listing
        products = soup.select("ul.products li.product, .products .product")
        if not products:
            products = soup.select(".product-inner, .product-item, article.product")

        for product in products[: self.max_results]:
            try:
                # Title
                title_el = product.select_one(
                    ".woocommerce-loop-product__title, .product-title a, h2 a, h3 a, .product-title"
                )
                title = title_el.get_text(strip=True) if title_el else "N/A"

                # Product URL
                link_el = product.select_one("a.woocommerce-LoopProduct-link, a[href]")
                product_url = link_el["href"] if link_el and link_el.get("href") else self.base_url

                # Price
                price_el = product.select_one(".price, .woocommerce-Price-amount")
                price = price_el.get_text(strip=True) if price_el else "N/A"

                # Image
                img_el = product.select_one("img")
                image_url = PLACEHOLDER_IMAGE
                if img_el:
                    image_url = img_el.get("src") or img_el.get("data-src") or PLACEHOLDER_IMAGE

                # Availability
                out_of_stock = bool(
                    product.select_one(".outofstock, .out-of-stock, .sold-out")
                )
                available = not out_of_stock

                results.append({
                    "title": title,
                    "price": price,
                    "available": available,
                    "image_url": image_url,
                    "product_url": product_url,
                    "store": self.store_name,
                })
            except Exception as e:
                logger.error("%s: Error parsing product: %s", self.store_name, e, exc_info=True)
                continue

        logger.info("%s: Found %d results for '%s'", self.store_name, len(results), query)
        return results
