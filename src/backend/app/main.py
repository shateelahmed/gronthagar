from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models import database, Book
# from app.migrations import upgrade_database
from fastapi.middleware.cors import CORSMiddleware
from .routers import books
from .config import settings

from alembic.config import Config
from alembic import command

from pathlib import Path
from logging.config import fileConfig
from os import path as os_path

ALEMBIC_INI_PATH = (Path(__file__).parent.parent / "../alembic.ini").resolve()
# ALEMBIC_INI_PATH = "../alembic.ini"
ALEMBIC_SCRIPT_LOCATION = "./migrations"

def run_migrations(script_location: str = ALEMBIC_SCRIPT_LOCATION) -> None:
    # LOG.info('Running DB migrations in %r on %r', script_location, settings.db_url)
    alembic_cfg = Config(ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', settings.db_url)
    fileConfig(os_path.join(os_path.dirname(os_path.abspath(__file__)), 'log.config'))
    command.upgrade(alembic_cfg, 'head')

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database.is_connected:
        await database.connect()
    run_migrations()
    await seed()
    yield
    if database.is_connected:
        await database.disconnect()

app = FastAPI(title="Gronthagar", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to {app.title}"}

@app.get("/seed")
async def seed():
    await Book.objects.get_or_create(
        title="some book",
        authors="shateel",
        summary="some story",
        publication_year=2000
    )

    return {
        "message": "Seeding successful",
        "data": None
    }
