from fastapi import FastAPI, Response, status
from app.models import database, Book
from ormar import NoMatch
from fastapi.middleware.cors import CORSMiddleware

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

def format_exception(exception: Exception) -> str:
    return f"An exception occurred. Exception type: {type(exception).__name__}. Arguments: {','.join(map(str, exception.args))}"

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

@app.get("/api/v1/books")
async def get_books(response: Response, q: str | None = None) -> Response:
    response.status_code = status.HTTP_404_NOT_FOUND
    message = "No books found"
    books = []

    try:
        if q:
            books = await database.fetch_all(
                """
                    SELECT
                        id,
                        title,
                        authors,
                        summary,
                        publication_year
                    FROM
                        books
                    WHERE
                        ts @@ plainto_tsquery(:q)
                """,
                {
                    'q': q
                }
            )
        else:
            books = await Book.objects.all()

        # books = await Book.objects.filter(
        #     ormar.or_(
        #         title__icontains=q,
        #         authors__icontains=q,
        #         summary__icontains=q
        #     )
        # ).get()
        if books:
            response.status_code = status.HTTP_200_OK
            message = "Books fetched successfully"
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = format_exception(exception)

    return {
        "message": message,
        "data": books
    }

@app.get("/api/v1/books/{id}")
async def get_book(id: int, response: Response) -> Response:
    book = {}

    try:
        book = await Book.objects.get(pk=id)
        response.status_code = status.HTTP_200_OK
        message = "Book fetched successfully"
    except NoMatch as ex:
        response.status_code = status.HTTP_404_NOT_FOUND
        message = "No book found"
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = format_exception(exception)

    return {
        "message": message,
        "data": book
    }

@app.post("/api/v1/books")
async def create_book(book: Book, response: Response) -> Response:
    try:
        book = await book.save()
        response.status_code = status.HTTP_201_CREATED
        message = "Book created successfully"
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = format_exception(exception)
        book = {}

    return {
        "message": message,
        "data": book
    }

@app.put("/api/v1/books/{id}")
async def update_book(id: int, book: Book, response: Response) -> Response:
    try:
        book_from_db = await Book.objects.get(pk=id)
        book.id = id
        book = await book_from_db.update(**book.dict())
        response.status_code = status.HTTP_200_OK
        message = "Book updated successfully"
    except NoMatch as ex:
        response.status_code = status.HTTP_404_NOT_FOUND
        message = f"Invalid book ID {id}"
        book = {}
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = format_exception(exception)
        book = {}

    return {
        "message": message,
        "data": book
    }

@app.delete("/api/v1/books/{id}")
async def delete_book(id: int, response: Response) -> Response:
    book = {}

    try:
        book_from_db = await Book.objects.get(pk=id)
        await book_from_db.delete()
        response.status_code = status.HTTP_200_OK
        message = "Book deleted successfully"
        book = book_from_db
    except NoMatch as ex:
        response.status_code = status.HTTP_404_NOT_FOUND
        message = f"Invalid book ID {id}"
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = format_exception(exception)

    return {
        "message": message,
        "data": book
    }
