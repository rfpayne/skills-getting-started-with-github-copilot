"""
Unit tests for the Mergington High School Activities Management System.

These tests validate the in-memory data structures and isolated business logic
without making HTTP requests.
"""

import sys
import os

# Ensure the src package is importable when running pytest from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.app import activities


# ---------------------------------------------------------------------------
# Unit tests – data structure
# ---------------------------------------------------------------------------

def test_activities_not_empty():
    """The initial activities dict must contain at least one activity."""
    assert len(activities) > 0


def test_each_activity_has_required_fields():
    """Every activity must have the four expected fields."""
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for name, details in activities.items():
        assert required_fields.issubset(details.keys()), (
            f"Activity '{name}' is missing one or more required fields."
        )


def test_participants_is_a_list():
    """The participants value for each activity must be a list."""
    for name, details in activities.items():
        assert isinstance(details["participants"], list), (
            f"Participants for '{name}' should be a list."
        )


def test_max_participants_is_positive_integer():
    """max_participants must be a positive integer for every activity."""
    for name, details in activities.items():
        assert isinstance(details["max_participants"], int), (
            f"max_participants for '{name}' should be an int."
        )
        assert details["max_participants"] > 0, (
            f"max_participants for '{name}' should be positive."
        )


def test_initial_participants_within_capacity():
    """Pre-seeded participants must not exceed the activity capacity."""
    for name, details in activities.items():
        assert len(details["participants"]) <= details["max_participants"], (
            f"Activity '{name}' already exceeds its max_participants."
        )


# ---------------------------------------------------------------------------
# Unit tests – business logic (direct dict manipulation)
# ---------------------------------------------------------------------------

def test_add_participant_directly():
    """Directly appending an email to participants should increase the count."""
    activity_name = next(iter(activities))
    before = len(activities[activity_name]["participants"])
    activities[activity_name]["participants"].append("test@mergington.edu")
    assert len(activities[activity_name]["participants"]) == before + 1


def test_activity_name_is_string():
    """All activity keys in the dict must be non-empty strings."""
    for name in activities:
        assert isinstance(name, str) and name, "Activity name must be a non-empty string."
