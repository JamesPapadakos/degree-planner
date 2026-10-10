# U of T Degree Planner

A backend application for tracking degree progress and checking course requirements for University of Toronto programs.

The application stores course and program data in PostgreSQL and uses FastAPI to expose REST API endpoints for retrieving courses, programs, and evaluating degree progress based on completed courses.

## Features

- View available courses
- View supported academic programs
- Check required courses for a program
- Check 300-level and 400-level credit requirements
- Check course-group requirements
- Validate course prerequisites
- Normalize course-code input such as `csc148` or `CSC 148`
- Detect invalid course codes
- Prevent duplicate courses from being counted multiple times
- REST API built with FastAPI
- Automated tests using pytest

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- psycopg
- Pydantic
- pytest
- Git / GitHub

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
├── .env
├── .gitignore
└── README.md
```

## Database

The PostgreSQL database stores:

- Courses
- Course prerequisites
- Academic programs
- Required courses
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

## API Endpoints

### Root

```http
GET /
```

Checks whether the API is running.

### Courses

```http
GET /courses
```

Returns all courses stored in the database.

### Programs

```http
GET /programs
```

Returns all supported academic programs.

### Program Requirements

```http
GET /programs/{program_id}
```

Returns the requirements for a selected program.

### Degree Check

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
      "completed": false
    }
  ],
  "course_groups": [
    {
      "name": "Upper Year Options",
      "completed_credits": 0.5,
      "required_credits": 1.0,
      "completed": false
    }
  ]
}
```

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd degree-planner
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn psycopg[binary] python-dotenv pytest httpx
```

### 3. Create the PostgreSQL database

Create a PostgreSQL database called:

```text
degree_planner
```

Run `schema.sql` to create the tables.

Then run `seed.sql` to insert sample data.

### 4. Create a `.env` file

Create a file called:

```text
.env
```

Add:

```text
DB_PASSWORD=your_postgresql_password
```

### 5. Start the API

```bash
uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

to use FastAPI's interactive API documentation.

## Running Tests

Run:

```bash
python -m pytest
```

## Future Improvements

- Build a frontend interface
- Add course search and autocomplete
- Support more University of Toronto programs
- Add semester planning
- Display overall degree progress
- Deploy the application online
- Add user accounts and saved degree plans
