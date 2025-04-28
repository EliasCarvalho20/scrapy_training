from itemadapter import ItemAdapter

from bookscraper.database.connection import get_session
from bookscraper.database.models import Books


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for f_name in field_names:
            if f_name != "description":
                adapter[f_name] = adapter.get(f_name).strip()

        # Category, Product & Stars Type --> switch to lowercase
        lowercase_keys = ["category", "product_type", "stars"]
        for l_key in lowercase_keys:
            adapter[l_key] = adapter.get(l_key).lower()

        # Price --> convert to float
        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for p_key in price_keys:
            adapter[p_key] = float(adapter.get(p_key).replace("£", ""))

        # Availability --> extract number of books in stock
        availability_split = adapter.get("availability").split("(")
        if len(availability_split) < 2:
            adapter["availability"] = 0
        else:
            adapter["availability"] = int(availability_split[1].split(" ")[0])

        # Reviews --> convert string to number
        adapter["num_reviews"] = int(adapter.get("num_reviews"))

        # Stars --> convert text to number
        stars_mapping = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
        }
        adapter["stars"] = stars_mapping.get(adapter.get("stars").split()[1])

        return item


class SaveToPostgresPipeline:
    def __init__(self):
        self.session = get_session()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        book_data = {
            "url": adapter["url"],
            "title": adapter.get("title"),
            "upc": adapter.get("upc"),
            "product_type": adapter.get("product_type"),
            "price": adapter.get("price"),
            "price_excl_tax": adapter.get("price_excl_tax"),
            "price_incl_tax": adapter.get("price_incl_tax"),
            "tax": adapter.get("tax"),
            "availability": adapter.get("availability"),
            "num_reviews": adapter.get("num_reviews"),
            "stars": adapter.get("stars"),
            "category": adapter.get("category"),
            "description": adapter.get("description"),
        }

        self.session.add(Books(**book_data))
        self.session.commit()

        return item
