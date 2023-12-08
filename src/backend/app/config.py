import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(
        f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOSTNAME')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )

settings = Settings()