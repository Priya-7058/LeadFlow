
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.main import app
from app.ai_service import classify_lead


# Create a separate database used only for tests.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Give the API a test database instead of the real database.
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to LeadFlow!",
        "status": "running"
    }


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_lead(monkeypatch):
    # Mock the AI service so this test doesn't call Gemini.
    def mock_classify_lead(enquiry):
        return {
            "classification": "High",
            "reason": "Strong buying intent.",
            "suggested_action": "Contact the customer."
        }

    monkeypatch.setattr("app.crud.classify_lead", mock_classify_lead)

    lead_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "phone": "9876543210",
        "company": "Test Company",
        "enquiry": "Interested in AI automation services"
    }

    response = client.post("/leads", json=lead_data)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert data["company"] == "Test Company"
    assert data["status"] == "New"
    assert "id" in data


def test_duplicate_email(monkeypatch):
        # Mock Gemini to keep this test fast and predictable.
    def mock_classify_lead(enquiry):
        return {
            "classification": "High",
            "reason": "Strong buying intent.",
            "suggested_action": "Contact the customer."
        }

    monkeypatch.setattr("app.crud.classify_lead", mock_classify_lead)
    
    lead_data = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "phone": "9876543210",
        "company": "Example Company",
        "enquiry": "Interested in AI automation services"
    }

    first_response = client.post("/leads", json=lead_data)

    assert first_response.status_code == 201

    second_response = client.post("/leads", json=lead_data)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "A lead with this email already exists."
    )



def test_create_lead_with_invalid_email():
    lead_data = {
        "name": "Test User",
        "email": "not-an-email",
        "phone": "9876543210",
        "company": "Test Company",
        "enquiry": "Interested in AI automation services"
    }

    response = client.post("/leads", json=lead_data)

    assert response.status_code == 422


def test_create_lead_with_short_name():
    lead_data = {
        "name": "A",
        "email": "shortname@example.com",
        "phone": "9876543210",
        "company": "Test Company",
        "enquiry": "Interested in AI automation services"
    }

    response = client.post("/leads", json=lead_data)

    assert response.status_code == 422


def test_create_lead_with_short_enquiry():
    lead_data = {
        "name": "Test User",
        "email": "shortenquiry@example.com",
        "phone": "9876543210",
        "company": "Test Company",
        "enquiry": "Hi"
    }

    response = client.post("/leads", json=lead_data)

    assert response.status_code == 422


def test_ai_classification_success(monkeypatch):
    # Fake Gemini's response so no real API call is made.
    def mock_classify_lead(enquiry):
        return {
            "classification": "High",
            "reason": "The customer has strong buying intent.",
            "suggested_action": "Contact the customer with pricing."
        }

    monkeypatch.setattr(
        "app.main.classify_lead",
        mock_classify_lead
    )

    response = client.post(
        "/leads/classify",
        json={
            "enquiry": "We want to buy your software this month."
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["classification"] == "High"
    assert data["reason"] == (
        "The customer has strong buying intent."
    )
    assert data["suggested_action"] == (
        "Contact the customer with pricing."
    )


def test_ai_classification_rejects_short_enquiry():
    response = client.post(
        "/leads/classify",
        json={"enquiry": "Hi"}
    )

    assert response.status_code == 422


def test_ai_classification_handles_service_failure(monkeypatch):
    # Simulate Gemini being unavailable.
    def mock_classify_lead(enquiry):
        raise RuntimeError("Simulated AI service failure")

    monkeypatch.setattr(
        "app.main.classify_lead",
        mock_classify_lead
    )

    response = client.post(
        "/leads/classify",
        json={
            "enquiry": "We are interested in your automation software."
        }
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "AI classification failed. Please try again later."
    )


def test_create_lead_when_ai_service_fails(monkeypatch):
    # Simulate Gemini being unavailable.
    def mock_classify_lead(enquiry):
        raise RuntimeError("Simulated AI service failure")

    # Replace the AI function used by the lead creation logic.
    monkeypatch.setattr(
        "app.crud.classify_lead",
        mock_classify_lead
    )

    lead_data = {
        "name": "Sneha Patil",
        "email": "sneha.failure@example.com",
        "phone": "9876543210",
        "company": "FutureTech",
        "enquiry": "We need automation solutions for our business."
    }

    response = client.post("/leads", json=lead_data)

    # The lead should still be created successfully.
    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Sneha Patil"
    assert data["email"] == "sneha.failure@example.com"

    # AI fields should remain empty when classification fails.
    assert data["ai_classification"] is None
    assert data["ai_reason"] is None
    assert data["ai_suggested_action"] is None