"""
Integration tests for the Mergington High School Activities Management System.

These tests exercise the full HTTP request/response cycle using FastAPI's
built-in TestClient (backed by httpx).
"""

import pytest
from fastapi.testclient import TestClient

import sys
import os

# Ensure the src package is importable when running pytest from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.app import app, activities

client = TestClient(app, follow_redirects=False)


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

def test_root_redirects_to_static():
    """GET / should return a redirect to /static/index.html."""
    response = client.get("/")
    assert response.status_code in (301, 302, 307, 308)
    assert "/static/index.html" in response.headers["location"]


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

def test_get_activities_returns_200():
    """GET /activities should return HTTP 200."""
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_json():
    """GET /activities should return a JSON object."""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)


def test_get_activities_contains_expected_activities():
    """GET /activities should include the pre-seeded activities."""
    response = client.get("/activities")
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_structure():
    """Each activity returned by the API must have the required fields."""
    response = client.get("/activities")
    data = response.json()
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for name, details in data.items():
        assert required_fields.issubset(details.keys()), (
            f"Activity '{name}' is missing required fields in the API response."
        )


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success():
    """Signing up with a valid activity and email should return HTTP 200."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_signup_adds_participant():
    """After a successful signup the email should appear in the participants list."""
    email = "newstudent@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404():
    """Signing up for a non-existent activity should return HTTP 404."""
    response = client.post(
        "/activities/Underwater Basket Weaving/signup",
        params={"email": "student@mergington.edu"},
    )
    assert response.status_code == 404


def test_signup_response_message_contains_email_and_activity():
    """The success message should reference both the email and the activity name."""
    email = "student@mergington.edu"
    activity = "Gym Class"
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    message = response.json()["message"]
    assert email in message
    assert activity in message


def test_signup_multiple_different_students():
    """Multiple different students should all be able to sign up for the same activity."""
    emails = ["alice@mergington.edu", "bob@mergington.edu"]
    for email in emails:
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email},
        )
        assert response.status_code == 200

    response = client.get("/activities")
    participants = response.json()["Programming Class"]["participants"]
    for email in emails:
        assert email in participants
