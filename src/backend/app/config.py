import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOSTNAME')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

    # if os.getenv('APP_ENV') == 'testing':
    #     db_url: str = f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('TEST_DATABASE_HOSTNAME')}:{os.getenv('TEST_DATABASE_PORT')}/{os.getenv('TEST_DATABASE_NAME')}"

settings = Settings()