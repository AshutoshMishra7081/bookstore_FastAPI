import pytest
import requests
import jwt
import time

BASE_URL = "http://127.0.0.1:8000"  # Change as per your server
LOGIN_ENDPOINT = "/login"
PROTECTED_ENDPOINT = "/protected"  # Change to an actual protected route

valid_user = {
    "email": "test@example.com",
    "password": "StrongPass123"
}

SECRET_KEY = "your_secret_key"  # Replace with actual secret key from your FastAPI app


def get_valid_token():
    """Helper function to get a valid JWT token"""
    response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=valid_user)
    assert response.status_code == 200, "Failed to login and get token"
    return response.json().get("access_token")


@pytest.mark.parametrize("token, expected_status, expected_message", [
    ("valid", 200, "Access granted"),
    ("expired", 401, "Token expired"),
    ("invalid", 401, "Invalid token"),
    (None, 401, "Authorization required"),
    ("no_permission", 403, "Forbidden")
])
def test_protected_route(token, expected_status, expected_message):
    """Test accessing a protected route with different authentication scenarios"""
    headers = {}

    if token == "valid":
        headers["Authorization"] = f"Bearer {get_valid_token()}"

    elif token == "expired":
        valid_token = get_valid_token()
        decoded_payload = jwt.decode(valid_token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        decoded_payload["exp"] = time.time() - 10  # Set expiry to past
        expired_token = jwt.encode(decoded_payload, SECRET_KEY, algorithm="HS256")
        headers["Authorization"] = f"Bearer {expired_token}"

    elif token == "invalid":
        headers["Authorization"] = "Bearer invalid.token.here"

    elif token == "no_permission":
        low_privilege_user = {
            "email": "restricted@example.com",
            "password": "StrongPass123"
        }
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=low_privilege_user)
        assert response.status_code == 200, "Failed to login low-privilege user"
        restricted_token = response.json().get("access_token")
        headers["Authorization"] = f"Bearer {restricted_token}"

    response = requests.get(f"{BASE_URL}{PROTECTED_ENDPOINT}", headers=headers)

    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    assert expected_message.lower() in response.text.lower(), f"Expected message '{expected_message}' not found"


if __name__ == "__main__":
    pytest.main(["-v", "test_protected_routes.py"])
