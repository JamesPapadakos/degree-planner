# U of T Degree Planner

A full-stack degree-planning application for University of Toronto students.

The application allows users to select an academic program, enter completed courses, and evaluate their progress toward program requirements. It uses a React frontend, FastAPI backend, and PostgreSQL database to track required courses, prerequisite relationships, upper-year credit requirements, and course-group requirements.

## Overview

The project was built to explore how degree requirements can be represented and evaluated programmatically.

Users can:

- Select a supported academic program
- Search and select completed courses
- Check required course completion
- Track 300-level and 400-level credit requirements
- Evaluate course-group requirements
- View prerequisite eligibility
- See remaining credits for incomplete requirements

The application also validates course input, normalizes course codes, and prevents duplicate courses from being counted multiple times.

## Tech Stack

### Frontend

- React
- JavaScript
- Vite
- CSS

### Backend

- Python
- FastAPI
- Pydantic

### Database

- PostgreSQL
- psycopg

### Testing and Development

- pytest
- FastAPI TestClient
- Git / GitHub
- Environment variables with `python-dotenv`

## Project Structure

```text
degree-planner/
├── api.py
├── database.py
├── main.py
├── requirements.py
├── schema.sql
├── seed.sql
├── Tests/
│   ├── test_api.py
│   └── test_requirements.py
├── frontend/
├── .gitignore
└── README.md
```

### `api.py`

Defines FastAPI endpoints and handles request validation and API error responses.

### `database.py`

Handles PostgreSQL connections and loads course, program, prerequisite, and requirement data.

### `requirements.py`

Contains the logic used to evaluate completed courses against program requirements.

### `frontend/`

Contains the React interface used to select programs, search courses, submit completed coursework, and display degree progress.

## Features

### Degree Requirement Checking

The application evaluates multiple requirement types:

- Mandatory courses
- Course-level credit requirements
- Course groups
- Course prerequisites

For example, a program can require:

```text
CSC236
CSC263

1.5 credits at the 300 level
2.0 credits at the 400 level

1.0 credits from:
CSC343
CSC369
CSC373
CSC384
```

The requirement engine evaluates the student's completed courses and returns structured progress information.

### Course Input Validation

Course codes are normalized before evaluation.

For example:

```text
csc148
CSC 148
Csc148
```

are all interpreted as:

```text
CSC148
```

Invalid course codes are rejected through the API, and duplicate courses are removed so they cannot be counted more than once.

### Course Search

The React frontend allows users to search courses by:

- Course code
- Course name

This makes course selection easier as the number of supported courses grows.

### Degree Progress Display

The frontend displays:

- Required courses that are completed or missing
- Credit progress for level-based requirements
- Remaining credits needed
- Course-group progress
- Visual progress bars for requirements

## Demo

### Course Search

![Course search](docs/course-search.png)

Search for courses by course code or course name and select completed courses.

### Degree Progress

![Degree progress](docs/degree-progress.png)

View completed and missing required courses, level-credit progress, and remaining credits.

## REST API

The FastAPI backend exposes endpoints for accessing application data and evaluating degree progress.

### Root

```http
GET /
```

Checks whether the API is running.

### Get Courses

```http
GET /courses
```

Returns all courses stored in the PostgreSQL database.

### Get Programs

```http
GET /programs
```

Returns all supported academic programs.

### Get Program Requirements

```http
GET /programs/{program_id}
```

Returns the requirements for a selected program.

### Check Degree Progress

```http
POST /degree-check
```

Example request:

```json
{
  "program_id": 1,
  "completed_courses": [
    "CSC148",
    "CSC236",
    "CSC343"
  ]
}
```

Example response:

```json
{
  "program_id": 1,
  "required_courses": [
    {
      "course": "CSC236",
      "completed": true
    },
    {
      "course": "CSC263",
      "completed": false
    }
  ],
  "level_requirements": [
    {
      "level": 300,
      "completed_credits": 0.5,
      "required_credits": 1.5,
      "remaining_credits": 1.0,
      "completed": false
    }
  ],
  "course_groups": [
    {
      "name": "Upper Year Options",
      "completed_credits": 0.5,
      "required_credits": 1.0,
      "remaining_credits": 0.5,
      "completed": false
    }
  ]
}
```

## Database Design

The PostgreSQL database stores:

- Courses
- Course prerequisites
- Academic programs
- Program-specific required courses
- Level-based credit requirements
- Course groups
- Course-group options

The database schema is defined in:

```text
schema.sql
```

Sample development data is included in:

```text
seed.sql
```

The database uses foreign keys to ensure that prerequisite and requirement relationships only reference valid courses and programs.

## Testing

The project includes automated tests for both requirement logic and API behavior.

Tests cover:

- Completed required courses
- Missing required courses
- Level-credit calculations
- Incomplete level requirements
- Course-group calculations
- Empty course selections
- Invalid program IDs
- Invalid course codes
- Course-code normalization
- API responses

Run the full test suite with:

```bash
python -m pytest
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd degree-planner
```

### 2. Install backend dependencies

```bash
pip install fastapi uvicorn "psycopg[binary]" python-dotenv pytest httpx
```

### 3. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
degree_planner
```

Run:

```text
schema.sql
```

to create the database tables.

Then run:

```text
seed.sql
```

to insert sample development data.

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
.env
```

Add:

```text
DB_PASSWORD=your_postgresql_password
```

The `.env` file is excluded from Git through `.gitignore`.

### 5. Start the backend

Run:

```bash
uvicorn api:app --reload
```

FastAPI will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open a second terminal and run:

```bash
cd frontend
npm install
npm run dev
```

Open the local Vite URL shown in the terminal, usually:

```text
http://localhost:5173
```

## Current Status

The project currently includes a working full-stack degree-checking workflow:

```text
React
  ↓
FastAPI
  ↓
Degree Requirement Evaluation
  ↓
PostgreSQL
```

Users can:

- Select an academic program
- Search available courses
- Select completed courses
- Submit degree progress checks
- View required courses that are complete or missing
- View credit progress toward level requirements
- View course-group progress
- See remaining credits needed

## Future Improvements

- Support additional University of Toronto programs
- Add semester-by-semester course planning
- Add overall degree completion percentage
- Support more complex prerequisite relationships
- Add user accounts and saved degree plans
- Deploy the application online
- Add frontend automated testing
- Expand course and program data coverage
