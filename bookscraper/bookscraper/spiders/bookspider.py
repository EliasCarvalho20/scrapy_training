import re
import scrapy
from urllib.parse import urljoin

from bookscraper.items import BookItem

URL = "http://books.toscrape.com/"


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [URL]

    def parse(self, response):
        catalogue_pattern = re.compile(r"catalogue/")
        for book in response.css("article.product_pod"):
            book_url = re.sub(
                catalogue_pattern, "", book.css("h3 > a::attr(href)").get()
            )
            yield response.follow(
                urljoin(URL, f"catalogue/{book_url}"), self.parse_book
            )

        try:
            next_page = re.sub(
                catalogue_pattern,
                "",
                response.css("li.next > a::attr(href)").get(),
            )
            next_page_url = urljoin(URL, f"catalogue/{next_page}")
            yield response.follow(next_page_url, self.parse)
        except TypeError:
            return

    def parse_book(self, response):
        table_rows = response.css("table tr")
        table_keys = [
            "upc",
            "product_type",
            "price_excl_tax",
            "price_incl_tax",
            "tax",
            "availability",
            "num_reviews",
        ]

        book_items = BookItem()
        for key, elem in zip(table_keys, table_rows):
            book_items[key] = elem.css("td::text").get()

        book_items["url"] = response.url
        book_items["title"] = response.css(".product_main h1::text").get()
        book_items["stars"] = response.css("p.star-rating").attrib["class"]
        book_items["price"] = response.css(
            ".product_main .price_color::text"
        ).get()
        book_items["category"] = response.xpath(
            '//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()'
        ).get()
        book_items["description"] = response.xpath(
            '//article[@class="product_page"]/p/text()'
        ).get()

        yield book_items
