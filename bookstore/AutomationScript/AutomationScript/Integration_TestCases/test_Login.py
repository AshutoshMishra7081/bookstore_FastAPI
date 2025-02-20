import pytest
import requests

# Base URL of your FastAPI application
BASE_URL = "http://127.0.0.1:8000"  # Change as per your server
ENDPOINT = "/login"

# Sample valid user credentials
valid_user = {
    "email": "test@example.com",
    "password": "StrongPass123"
}

# 🚀 Test cases for user login
@pytest.mark.parametrize("test_data, expected_status, expected_message", [
    # Login with correct credentials (Successful authentication)
    (valid_user, 200, "access_token"),

    # Login with incorrect email
    ({"id": 0, "email": "wrong@example.com", "password": "StrongPass123"}, 401, "Invalid email or password"),

    # Login with incorrect password
    ({"id": 0, "email": "test@example.com", "password": "WrongPass"}, 401, "Invalid email or password"),

    # Login with unregistered email
    ({"id": 0, "email": "unregistered@example.com", "password": "SomePass123"}, 401, "User not found"),

    # Login with missing email field
    ({"id": 0, "password": "StrongPass123"}, 400, "Email is required"),

    # Login with missing password field
    ({"id": 0, "email": "test@example.com"}, 400, "Password is required"),

    # Login with an empty request body
    ({}, 400, "Request body cannot be empty"),

    # Login with an invalid email format
    ({"id": 0, "email": "invalid-email", "password": "ValidPass123"}, 400, "Invalid email format"),

    # Login with a deactivated user (if applicable)
    ({"id": 0, "email": "deactivated@example.com", "password": "StrongPass123"}, 403, "User account is deactivated"),

    # Login with an expired JWT token (if session handling is implemented)
    ({"id": 0, "email": "expired@example.com", "password": "StrongPass123"}, 401, "Token expired, please login again"),
])
def test_login_user(test_data, expected_status, expected_message):
    """Test user login with different scenarios"""
    response = requests.post(f"{BASE_URL}{ENDPOINT}", json=test_data)

    print(response)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    assert expected_message.lower() in response.text.lower(), f"Expected message '{expected_message}' not found"


if __name__ == "__main__":
    pytest.main(["-v", "test_login.py"])  # Run tests with verbose output
