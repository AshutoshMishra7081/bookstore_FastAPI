import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"  # Update if needed
UPDATE_BOOK_ENDPOINT = "/books/{book_id}"

# Sample valid book update data
valid_book_update = {
    "id": 1,
    "name": "Updated Book Title",
    "author": "Updated Author",
    "published_year": 2025,
    "book_summary": "An updated summary of the book."
}


@pytest.mark.parametrize("book_id, update_data, headers, expected_status, expected_response", [
    # ✅ Update a book successfully (200)
    (1, valid_book_update, {"Authorization": "Bearer VALID_TOKEN"}, 200, "Book updated successfully"),

    # ❌ Update a book that doesn’t exist (404)
    (999, valid_book_update, {"Authorization": "Bearer VALID_TOKEN"}, 404, "Book not found"),

    # ❌ Update a book with missing title (422 Validation Error)
    (1, {"id": 1, "author": "Updated Author", "published_year": 2025, "book_summary": "Summary"},
     {"Authorization": "Bearer VALID_TOKEN"}, 422, "Validation Error"),

    # ❌ Update a book with missing author (422 Validation Error)
    (1, {"id": 1, "name": "Updated Title", "published_year": 2025, "book_summary": "Summary"},
     {"Authorization": "Bearer VALID_TOKEN"}, 422, "Validation Error"),

    # ❌ Unauthorized request - No token provided (403)
    (1, valid_book_update, {}, 403, "Forbidden"),

    # ❌ Expired/Invalid token (403)
    (1, valid_book_update, {"Authorization": "Bearer INVALID_TOKEN"}, 403, "Forbidden"),
])
def test_update_book(book_id, update_data, headers, expected_status, expected_response):
    """Test updating a book with different scenarios"""
    response = requests.put(f"{BASE_URL}{UPDATE_BOOK_ENDPOINT.format(book_id=book_id)}", json=update_data,
                            headers=headers)
    print(response)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

    if expected_response == "Validation Error":
        assert response.status_code == 422, "Expected validation error but got a different response."
    elif expected_response == "Book updated successfully":
        assert "updated" in response.text.lower(), "Expected book update confirmation but got something else."
    elif expected_response == "Book not found":
        assert response.status_code == 404, "Expected 404 for non-existent book."
    elif expected_response == "Forbidden":
        assert response.status_code == 403, "Expected forbidden access response."


if __name__ == "__main__":
    pytest.main(["-v", "test_update_book.py"])
