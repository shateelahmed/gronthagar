from fastapi.testclient import TestClient
from ..main import app, seed

client = TestClient(app)

seed()

def test_get_books():
    response = client.get("/api/v1/books")
    assert response.status_code == 200

def test_get_book():
    response = client.get("/api/v1/books/1")
    assert response.status_code == 200

def test_create_book():
    data = {
        "title": "Harry Potter And The Prisoner of Azkaban",
        "authors": "J. K. Rowling",
        "summary": "The content of Harry Potter And The Prisoner of Azkaban by J. K. Rowling",
        "publication_year": 2001
    }
    response = client.post("/api/v1/books", json=data)
    print(response.json())
    assert response.status_code == 201

def test_create_book_with_invalid_payload():
    data = {
        "title": "Harry Potter And The Prisoner of Azkaban",
        "authors": "J. K. Rowling",
        "summary": "The content of Harry Potter And The Prisoner of Azkaban by J. K. Rowling",
    }
    response = client.post("/api/v1/books", json=data)
    print(response.json())
    assert response.status_code == 422

def test_update_book():
    data = {
        "title": "Harry Potter And The Prisoner of Azkaban",
        "authors": "J. K. Rowling",
        "summary": "The content of Harry Potter And The Prisoner of Azkaban by J. K. Rowling",
        "publication_year": 2001
    }
    response = client.put("/api/v1/books/1", json=data)
    print(response)
    assert response.status_code == 200

def test_update_book_invalid_payload():
    data = {
        "title": "Harry Potter And The Prisoner of Azkaban",
        "authors": "J. K. Rowling",
        "publication_year": 2001
    }
    response = client.put("/api/v1/books/1", json=data)
    print(response)
    assert response.status_code == 422

def test_delete_book():
    response = client.delete("/api/v1/books/1")
    print(response)
    assert response.status_code == 200

def test_delete_book_invalid_book():
    response = client.delete("/api/v1/books/2")
    print(response)
    assert response.status_code == 404