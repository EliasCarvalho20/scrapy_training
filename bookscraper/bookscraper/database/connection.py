from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bookscraper.database.env_settings import EnvSettings
from bookscraper.database.models import table_registry


engine = create_engine(EnvSettings().DATABASE_URL)
table_registry.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        return session
