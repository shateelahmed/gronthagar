import databases
import ormar
import sqlalchemy
from datetime import datetime

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


# class User(ormar.Model):
#     class Meta(BaseMeta):
#         tablename = "users"

#     id: int = ormar.Integer(primary_key=True)
#     email: str = ormar.String(max_length=128, unique=True, nullable=False)
#     active: bool = ormar.Boolean(default=True, nullable=False)


class Book(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'books'

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=128, unique=True, nullable=False)
    authors: str = ormar.String(max_length=256, nullable=False)
    summary: str = ormar.String(max_length=512, nullable=False)
    publication_year: int = ormar.Integer(max=datetime.now().year, nullable=False)


# engine = sqlalchemy.create_engine(settings.db_url)
# metadata.create_all(engine)