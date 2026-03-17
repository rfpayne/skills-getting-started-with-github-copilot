# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Architecture](#architecture)

## Features

- View all available extracurricular activities
- Sign up for activities

## Project Structure

```
src/
├── app.py          # FastAPI application – defines routes and in-memory data store
└── static/
    ├── index.html  # Single-page frontend
    ├── styles.css  # Stylesheet for the frontend
    └── app.js      # Client-side logic (fetches activities, handles sign-up form)
```

## Getting Started

1. Install the dependencies:

   ```bash
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```bash
   uvicorn app:app --reload
   ```

3. Open your browser and go to:
   - **Frontend:** http://localhost:8000
   - **Interactive API docs (Swagger UI):** http://localhost:8000/docs
   - **Alternative API docs (ReDoc):** http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

### Example Requests

**Get all activities**
```bash
curl http://localhost:8000/activities
```

**Sign up for an activity**
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=student@mergington.edu"
```

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** – uses activity name as identifier:

   | Field              | Type         | Description                              |
   | ------------------ | ------------ | ---------------------------------------- |
   | `description`      | `str`        | Short summary of the activity            |
   | `schedule`         | `str`        | Days and times the activity meets        |
   | `max_participants` | `int`        | Maximum number of students allowed       |
   | `participants`     | `list[str]`  | Email addresses of enrolled students     |

2. **Students** – identified by email address:
   - Name
   - Grade level

> **Note:** All data is stored in memory, which means data will be reset when the server restarts.

## Architecture

```
Browser  ──GET /──►  FastAPI  ──►  Redirect to /static/index.html
                        │
           GET /activities        Returns JSON activity data
                        │
         POST /activities/{name}/signup   Adds student email to activity
```

The frontend (`index.html` + `app.js`) communicates with the backend through the REST API.  
Static assets are served directly by FastAPI using `StaticFiles`.

