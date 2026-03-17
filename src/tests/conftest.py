"""
Shared pytest fixtures for the Mergington High School test suite.
"""

import copy
import pytest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.app import activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the activities dict to its original state after every test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
