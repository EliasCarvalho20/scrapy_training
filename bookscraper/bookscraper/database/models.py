from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Books:
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    upc: Mapped[str]
    product_type: Mapped[str]
    price: Mapped[float]
    price_excl_tax: Mapped[float]
    price_incl_tax: Mapped[float]
    tax: Mapped[float]
    availability: Mapped[int]
    num_reviews: Mapped[int]
    stars: Mapped[int]
    category: Mapped[str]
    url: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
