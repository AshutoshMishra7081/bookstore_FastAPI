import pytest
import requests

# Base URL of your FastAPI application
BASE_URL = "http://127.0.0.1:8000"  # Change as per your server
ENDPOINT = "/signup"



# 🚀 Test cases for user registration
@pytest.mark.parametrize("test_data, expected_status, expected_message", [
    # Register a new user successfully
    ({"id": 1, "email": "test@example.com", "password": "StrongPass123"}, 201, "User created successfully"),

    # Register with an already existing email
    ({"id": 2, "email": "test@example.com", "password": "AnotherPass123"}, 400, "User with this email already exists"),

    # Register with an invalid email format
    ({"id": 3, "email": "invalid-email", "password": "StrongPass123"}, 400, "Invalid email format"),

    # Register with a weak password (too short)
    ({"id": 4, "email": "newuser@example.com", "password": "123"}, 400, "Password too weak"),

    # Register without an email
    ({"id": 5, "password": "StrongPass123"}, 400, "Email is required"),

    # Register without a password
    ({"id": 6, "email": "newuser@example.com"}, 400, "Password is required"),

    # Register with an empty request body
    ({}, 400, "Request body cannot be empty")
])
def test_register_user(test_data, expected_status, expected_message):
    """Test user registration with different scenarios"""
    response = requests.post(f"{BASE_URL}{ENDPOINT}", json=test_data)  # 🔹 Using correct test_data

    print(response)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    assert expected_message.lower() in response.text.lower(), f"Expected message '{expected_message}' not found in response '{response.text}'"


if __name__ == "__main__":
    pytest.main(["-v"])  # Run tests with verbose output
