## FastAPI Bookstore Automation Testing

### Overview
This repository contains automation test scripts for the **FastAPI Bookstore Application**. The test suite includes **unit, integration, and API testing**, ensuring the reliability and correctness of the application.

### Features
- **Unit Testing** - Validates core business logic.
- **Integration Testing** - Ensures proper API functionality.
- **API Testing** - Tests authentication, CRUD operations, and error handling.
- **Mocking** - Uses dependency injection for better test isolation.
- **CI/CD Integration** - Automated test execution using **GitHub Actions**.

### Technologies Used
- **FastAPI** - High-performance API framework.
- **MongoDB (Motor)** - Asynchronous database operations.
- **Pytest** - Unit and integration testing framework.
- **Httpx** - API testing client.
- **GitHub Actions** - CI/CD automation.

---

## Getting Started

### Prerequisites
- **Python 3.7+** installed.
- **MongoDB** running locally or in a Docker container.

### Installation
```bash
# Clone the repository
git clone https://github.com/AshutoshMishra7081/bookstore_FastAPI.git
cd bookstore/AutomationScript/AutomationScript

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Running Tests

### Run Unit Tests
```bash
pytest -v Test_Cases.py --cov=app --cov-report=term-missing
```

### Run Integration Tests
cd $PWD/bookstore/AutomationScript/AutomationScript/Integration_TestCases
```bash
pytest -v test_SignUp.py
pytest -v test_Login.py
pytest -v test_APIResponseAndErrorHandling.py
pytest -v test_AddingBooks.py
pytest -v test_TokenGeneration.py
pytest -v test_UpdateBooks.py
pytest -v test_DeleteBook.py
pytest -v test_RetrievingBooks.py
pytest -v test_ProtectedRoutes.py
```

### Run API Tests
```bash
pytest - tests/api
```

### Run Full Test Suite
```bash
pytest -v $PWD/bookstore/AutomationScript/AutomationScript
```

---

## API Endpoints Tested

### User Authentication
- `POST /signup` - Register a new user.
- `POST /login` - Authenticate and receive JWT token.

### Book Management
- `POST /books/` - Add a new book.
- `GET /books/` - Retrieve all books.
- `GET /books/{book_id}` - Get a book by ID.
- `PUT /books/{book_id}` - Update book details.
- `DELETE /books/{book_id}` - Delete a book.

### Protected Routes (JWT Authentication)
- Unauthorized access testing.
- Expired/invalid token handling.

### Health Check
- `GET /health` - Check API health status.

---

## CI/CD Pipeline (GitHub Actions)
This project includes a **GitHub Actions CI/CD pipeline** that:
- Runs **unit and integration tests** on each commit.
- Ensures **code coverage meets required thresholds**.
- Prevents deployments if tests fail.

---

## Testing Strategy

### Unit Testing
- Validates **business logic** and **utility functions**.
- Mocks external dependencies like **database interactions**.

### Integration Testing
- Tests **end-to-end API interactions**.
- Ensures **MongoDB queries execute correctly**.

### API Testing
- Tests **authentication workflows**.
- Validates **CRUD operations** with expected responses.
- Handles **unauthorized and invalid requests**.

---

## Running with Docker

### Start FastAPI and MongoDB with Docker
```bash
docker-compose up --build -d bookstore
```

### Run Tests Inside Docker
```bash
docker exec -it bookstore pytest
```

---

## Common Issues & Solutions

### 1. Commit & Push Issues
```bash
# If you cloned instead of forking, create a new fork and set the correct origin
git remote set-url origin https://github.com/AshutoshMishra7081/bookstore_FastAPI.git
```

### 2. MongoDB Connection Errors
```bash
# Ensure MongoDB is running locally or via Docker
docker-compose up -d
```

### 3. Tests Failing Due to Authentication
- Ensure you’re using a **valid JWT token** for protected endpoints.

---

### Alternatively you can run test cases directly from outside by just running those script in ide like Pycharm just open it and run it one by one to get the results

## How to Contribute?
1. **Fork** the repository.
2. **Create a new branch** (`git checkout -b feature-branch`).
3. **Commit changes** (`git commit -m "Added new test cases"`).
4. **Push to GitHub** and create a **pull request**.
---
