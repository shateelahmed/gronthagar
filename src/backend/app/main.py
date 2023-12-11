from fastapi import FastAPI
from app.models import database, Book
from fastapi.middleware.cors import CORSMiddleware
from .routers import books

app = FastAPI(title="Gronthagar")

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

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    await seed()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

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
