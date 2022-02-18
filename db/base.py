import databases
import ormar
import sqlalchemy

from core.config import settings

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata
