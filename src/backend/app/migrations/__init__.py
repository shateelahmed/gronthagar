from alembic import command
from alembic.config import Config

from app.config import settings


def get_alembic_config(db_url: str = settings.db_url) -> Config:
    alembic_config = Config()
    alembic_config.set_main_option("script_location", "app:migrations")
    alembic_config.set_main_option("sqlalchemy.url", db_url)
    return alembic_config


def upgrade_database(revision: str = "head", db_url: str = settings.db_url) -> None:
    alembic_config = get_alembic_config(db_url)
    command.upgrade(alembic_config, revision)


def downgrade_database(revision: str = "base", db_url: str = settings.db_url) -> None:
    alembic_config = get_alembic_config(db_url)
    command.upgrade(alembic_config, revision)