from fastapi import FastAPI
from app.models import database, Book

app = FastAPI(title="Gronthagar")


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await Book.objects.get_or_create(title="some book", authors="shateel", content="some story", publication_year=2000)

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

@app.get("/")
async def read_root():
    return await Book.objects.all()