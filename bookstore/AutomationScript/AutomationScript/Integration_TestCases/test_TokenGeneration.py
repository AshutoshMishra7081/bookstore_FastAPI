import pytest
import requests
import jwt
import time

# Base URL of your FastAPI application
BASE_URL = "http://127.0.0.1:8000"  # Change as per your server
LOGIN_ENDPOINT = "/login"
PROTECTED_ENDPOINT = "/protected"  # Change to an actual protected route if applicable

# Sample valid user credentials
valid_user = {
    "email": "test@example.com",
    "password": "StrongPass123"
}

# Secret key (should be fetched dynamically if possible)
SECRET_KEY = "your_secret_key"  # Replace with actual secret key used in your application


# 🚀 Test cases for JWT Token & Authorization
@pytest.mark.parametrize("test_data, expected_status, expected_message", [
    # Generate a valid JWT token for a registered user
    (valid_user, 200, "access_token"),

    # Generate a token with invalid payload data
    ({"email": "test@example.com", "password": "WrongPass"}, 401, "Invalid email or password"),

    # Generate a token for a non-existent user
    ({"email": "nonexistent@example.com", "password": "SomePass123"}, 401, "User not found"),

])
def test_generate_jwt_token(test_data, expected_status, expected_message):
    """Test JWT token generation"""
    response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=test_data)

    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    assert expected_message.lower() in response.text.lower(), f"Expected message '{expected_message}' not found"

    # If token is generated, validate structure
    if response.status_code == 200:
        token = response.json().get("access_token")
        assert token is not None, "Token was not generated"
        assert isinstance(token, str), "Generated token is not a string"


def test_token_expiration():
    """Ensure token expiration works correctly"""
    # Generate a valid token first
    login_response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=valid_user)

    assert login_response.status_code == 200, "Failed to login and get token"

    token = login_response.json().get("access_token")

    # Decode token and modify expiration to a past time (simulating expiration)
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
    decoded_payload["exp"] = time.time() - 10  # Set expiry to past

    expired_token = jwt.encode(decoded_payload, SECRET_KEY, algorithm="HS256")

    # Try accessing a protected route with expired token
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = requests.get(f"{BASE_URL}{PROTECTED_ENDPOINT}", headers=headers)

    assert response.status_code == 401, "Expired token should not be accepted"
    assert "Token expired" in response.text, "Expected 'Token expired' message not found"


if __name__ == "__main__":
    pytest.main(["-v", "test_jwt.py"])  # Run tests with verbose output
