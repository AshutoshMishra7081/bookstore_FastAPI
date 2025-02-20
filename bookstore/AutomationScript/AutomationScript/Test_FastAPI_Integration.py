import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_db
from database import UserCredentials, Book
from utils import create_access_token

# Test Database Setup
test_engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(test_engine)


# Override get_db dependency to use test database
def override_get_db():
    session = Session(test_engine)
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# Test User Signup
def test_signup(client):
    response = client.post("/signup", json={"email": "test@example.com", "password": "test123"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


# Test User Login
def test_login(client):
    response = client.post("/login", json={"email": "test@example.com", "password": "test123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test JWT Token Generation
def test_jwt_token():
    token = create_access_token({"sub": "test@example.com"})  # Pass a dictionary instead of a string
    assert isinstance(token, str)


# Test Adding a Book
def test_add_book(client):
    token = create_access_token({"sub": "test@example.com"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/add_book", json={"title": "FastAPI Guide", "author": "John Doe"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"


# Test Getting Books
def test_get_books(client):
    token = create_access_token({"sub": "test@example.com"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/get_books", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test Unauthorized Access
def test_unauthorized_access(client):
    response = client.get("/get_books")
    assert response.status_code == 401
