import pytest
from sqlmodel import Session, SQLModel, create_engine
from database import get_db
from database import UserCredentials, Book

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Create a new test session
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)  # Create tables
    with Session(engine) as session:
        yield session  # Provide session for test cases


# Test Case 1: Check if UserCredentials model stores data correctly
def test_create_user(session):
    user = UserCredentials(email="test@example.com", password="securepassword")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.password == "securepassword"  # Note: Hashing should be added later


# Test Case 2: Check if Book model stores data correctly
def test_create_book(session):
    book = Book(name="Python Basics", author="John Doe", published_year=2023, book_summary="Intro to Python")
    session.add(book)
    session.commit()
    session.refresh(book)

    assert book.id is not None
    assert book.name == "Python Basics"
    assert book.author == "John Doe"
    assert book.published_year == 2023


# Test Case 3: Ensure unique email constraint works
def test_unique_user_email(session):
    user1 = UserCredentials(email="unique@example.com", password="pass123")
    user2 = UserCredentials(email="unique@example.com", password="pass456")

    session.add(user1)
    session.commit()

    with pytest.raises(Exception):  # Should fail due to unique constraint
        session.add(user2)
        session.commit()
