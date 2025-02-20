import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"  # Update if needed
DELETE_BOOK_ENDPOINT = "/books/{book_id}"

@pytest.mark.parametrize("book_id, headers, expected_status, expected_response", [
    # ✅ Delete a book successfully (200)
    (1, {"Authorization": "Bearer VALID_TOKEN"}, 200, "Book deleted successfully"),

    # ❌ Delete a book that doesn’t exist (404)
    (999, {"Authorization": "Bearer VALID_TOKEN"}, 404, "Book not found"),

    # ❌ Unauthorized request - No token provided (403)
    (1, {}, 403, "Forbidden"),

    # ❌ Expired/Invalid token (403)
    (1, {"Authorization": "Bearer INVALID_TOKEN"}, 403, "Forbidden"),
])
def test_delete_book(book_id, headers, expected_status, expected_response):
    """Test deleting a book with different scenarios"""
    response = requests.delete(f"{BASE_URL}{DELETE_BOOK_ENDPOINT.format(book_id=book_id)}", headers=headers)

    print(response)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

    if expected_response == "Book deleted successfully":
        assert "deleted" in response.text.lower(), "Expected book deletion confirmation but got something else."
    elif expected_response == "Book not found":
        assert response.status_code == 404, "Expected 404 for non-existent book."
    elif expected_response == "Forbidden":
        assert response.status_code == 403, "Expected forbidden access response."

if __name__ == "__main__":
    pytest.main(["-v", "test_delete_book.py"])
