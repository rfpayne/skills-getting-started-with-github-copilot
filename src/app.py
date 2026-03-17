"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

The API stores activity and participant data in memory. All data is reset
when the server restarts.

Usage:
    uvicorn app:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory so the frontend (HTML/CSS/JS) is served
# from the /static route.
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database.
# Each key is the activity name, and the value is a dict with:
#   - description (str): Short summary of the activity
#   - schedule (str): When the activity meets
#   - max_participants (int): Maximum number of students allowed
#   - participants (list[str]): Emails of currently enrolled students
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    """Redirect the root URL to the frontend application.

    Returns:
        RedirectResponse: A 307 redirect to the static index page.
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return all available extracurricular activities.

    Returns:
        dict: A dictionary mapping activity names to their details, including
              description, schedule, maximum participants, and current participants.
    """
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity.

    Args:
        activity_name (str): The name of the activity to sign up for.
        email (str): The student's school email address.

    Returns:
        dict: A confirmation message indicating the student was signed up,
              e.g. ``{"message": "Signed up student@mergington.edu for Chess Club"}``.

    Raises:
        HTTPException: 404 if the activity does not exist.

    Note:
        This endpoint does not validate the email format, check for duplicate
        sign-ups, or enforce the ``max_participants`` limit.
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student to the participants list
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
