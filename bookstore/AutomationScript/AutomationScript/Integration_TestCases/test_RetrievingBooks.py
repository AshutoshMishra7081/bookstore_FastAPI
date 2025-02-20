import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"  # Change if needed
GET_BOOKS_ENDPOINT = "/books/"


@pytest.mark.parametrize("headers, expected_status, expected_response", [
    # ✅ Retrieve books when books exist (200)
    ({}, 200, "non-empty list"),

    # ✅ Retrieve books when no books exist (200, but empty list)
    ({}, 200, "empty list"),

    # ❌ Unauthorized request (403) - No token provided
    ({"Authorization": ""}, 403, "Forbidden"),

    # ❌ Expired/Invalid token (403)
    ({"Authorization": "Bearer INVALID_TOKEN"}, 403, "Forbidden"),
])
def test_get_books(headers, expected_status, expected_response):
    """Test retrieving books with different scenarios"""
    response = requests.get(f"{BASE_URL}{GET_BOOKS_ENDPOINT}", headers=headers)

    print(response)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

    if expected_response == "empty list":
        assert response.json() == [], "Expected an empty list, but got something else."
    elif expected_response == "non-empty list":
        assert isinstance(response.json(), list) and len(response.json()) > 0, "Expected a list with books."


if __name__ == "__main__":
    pytest.main(["-v", "test_get_books.py"])
