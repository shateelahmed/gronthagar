from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models import database, Book
from fastapi.middleware.cors import CORSMiddleware
from .routers import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database.is_connected:
        await database.connect()
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

async def seed():
    result = await Book.objects.get_or_create(
        title="some book",
        authors="shateel",
        summary="some story",
        publication_year=2000
    )
    return result[0]
