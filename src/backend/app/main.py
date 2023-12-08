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
    return {"message": f"Welcome to {app.title}"}

@app.get("/books")
async def get_books():
    books = await Book.objects.all()
    return {"data": books}

@app.get("/books/{id}")
async def get_book(id: int):
    return await Book.objects.get(pk=id)

@app.post("/books")
async def create_book(book: Book):
    await book.save()
    return book

@app.put("/books/{id}")
async def update_book(id: int, book: Book):
    book_from_db = await Book.objects.get(pk=id)
    book.id = id
    return await book_from_db.update(**book.dict())

@app.delete("/books/{id}")
async def delete_book(id: int):
    book_from_db = await Book.objects.get(pk=id)
    await book_from_db.delete()
    return {"deleted_book": book_from_db}