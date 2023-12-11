from fastapi import APIRouter, Response, status
from app.models import database, Book
from ormar import NoMatch
from ..utils.formatter import format_exception

router = APIRouter(
    prefix="/api/v1/books",
    tags=["books"],
)

@router.get("/")
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

@router.get("/{id}")
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

@router.post("/")
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

@router.put("/{id}")
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

@router.delete("/{id}")
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