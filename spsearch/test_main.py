from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models.search_request import SearchRequest, SearchType
from main import app

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

# Create the test database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)


# Test case for the search endpoint (keyword search)
def test_search_keyword():
    search_request = {
        "query": "test keyword",
        "search_type": "keyword"
    }
    response = client.post("/search", json=search_request)
    assert response.status_code == 200
    assert "results" in response.json()
    # Teardown: Clean up the test database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Test case for the search endpoint (vector search)
def test_search_vector():
    search_request = {
        "query": "test vector",
        "search_type": "vector"
    }
    response = client.post("/search", json=search_request)
    assert response.status_code == 200
    assert "results" in response.json()
    # Teardown: Clean up the test database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Test case for the search endpoint (hybrid search)
def test_search_hybrid():
    search_request = {
        "query": "test hybrid",
        "search_type": "hybrid"
    }
    response = client.post("/search", json=search_request)
    assert response.status_code == 200
    assert "results" in response.json()
    # Teardown: Clean up the test database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Test case for invalid search type
def test_search_invalid_type():
    search_request = {
        "query": "test invalid",
        "search_type": "invalid"
    }
    response = client.post("/search", json=search_request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid search type"}

# Test case for non-existent endpoint
def test_non_existent_endpoint():
    response = client.get("/non_existent_endpoint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

# Run the tests
if __name__ == "__main__":
    test_search_keyword()
    test_search_vector()
    test_search_hybrid()
    test_search_invalid_type()
    test_non_existent_endpoint()
