import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"  # Change if needed
ADD_BOOK_ENDPOINT = "/books/"

valid_book = {
    "id": 1,
    "name": "The Art of Testing",
    "author": "John Doe",
    "published_year": 2024,
    "book_summary": "A complete guide to software testing methodologies."
}


@pytest.mark.parametrize("book_data, expected_status", [
    # ✅ Successful case (200)
    (valid_book, 200),

    # ❌ Missing name (422)
    ({"id": 2, "author": "John Doe", "published_year": 2024, "book_summary": "Summary"}, 422),

    # ❌ Missing author (422)
    ({"id": 3, "name": "The Art of Testing", "published_year": 2024, "book_summary": "Summary"}, 422),

    # ❌ Missing published_year (422)
    ({"id": 4, "name": "The Art of Testing", "author": "John Doe", "book_summary": "Summary"}, 422),

    # ❌ Missing book_summary (422)
    ({"id": 5, "name": "The Art of Testing", "author": "John Doe", "published_year": 2024}, 422),

    # ❌ Empty request body (422)
    ({}, 422),

    # ❌ Unauthorized request (403) → No authentication (if required)
    (valid_book, 403),
])
def test_add_book(book_data, expected_status):
    """Test adding a book with different scenarios"""
    response = requests.post(f"{BASE_URL}{ADD_BOOK_ENDPOINT}", json=book_data)

    print(response)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"


if __name__ == "__main__":
    pytest.main(["-v", "test_add_book.py"])
