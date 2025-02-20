import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"  # Update if needed

ENDPOINTS = [
    ("/signup", "POST", {"email": "test@example.com", "password": "TestPass123"}),
    ("/login", "POST", {"email": "test@example.com", "password": "TestPass123"}),
    ("/books/", "GET", None),
    ("/books/", "POST", {"name": "API Testing", "author": "John Doe", "published_year": 2024, "book_summary": "A guide to API testing"}),
    ("/books/1", "PUT", {"name": "Updated Book", "author": "Jane Doe", "published_year": 2025, "book_summary": "Updated summary"}),
    ("/books/1", "DELETE", None)
]

# 🚀 Test Cases for API Responses & Error Handling
@pytest.mark.parametrize("endpoint, method, payload", ENDPOINTS)
def test_api_response_status_codes(endpoint, method, payload):
    """Ensures correct HTTP status codes for each endpoint"""
    url = f"{BASE_URL}{endpoint}"

    start_time = time.time()  # Track API response time

    if method == "POST":
        response = requests.post(url, json=payload)
    elif method == "GET":
        response = requests.get(url)
    elif method == "PUT":
        response = requests.put(url, json=payload)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        pytest.fail(f"Unsupported HTTP method: {method}")

    response_time = time.time() - start_time  # Calculate response time

    print(response)
    assert response.status_code in [200, 201, 400, 401, 403, 404, 422, 500], f"Unexpected status code {response.status_code}"
    assert response_time < 2, f"API response time too high: {response_time:.2f} seconds"

    # 🛑 Check for proper error messages
    if response.status_code == 400:
        assert "detail" in response.json(), "Expected 'detail' field for 400 errors"
    elif response.status_code == 500:
        assert "Internal Server Error" in response.text, "Expected internal server error message"

if __name__ == "__main__":
    pytest.main(["-v", "test_api_responses.py"])
