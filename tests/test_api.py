from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Degree Planner API is running"
    }

def test_courses():
    response = client.get("/courses")

    assert response.status_code == 200

    data = response.json()

    assert "CSC343" in data
    assert data["CSC343"]["credits"] == 0.5

def test_degree_check():
    response = client.post(
        "/degree-check",
        json={
            "program_id": 1,
            "completed_courses": [
                "CSC148",
                "CSC236",
                "CSC343"
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["program_id"] == 1
    assert "required_courses" in data
    assert "level_requirements" in data
    assert "course_groups" in data

def test_invalid_program():
    response = client.post(
        "/degree-check",
        json={
            "program_id": 999,
            "completed_courses": ["CSC148"]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Program not found"

def test_invalid_course():
    response = client.post(
        "/degree-check",
        json={
            "program_id": 1,
            "completed_courses": [
                "CSC148",
                "CSC999"
            ]
        }
    )

    assert response.status_code == 400

def test_course_normalization():
    response = client.post(
        "/degree-check",
        json={
            "program_id": 1,
            "completed_courses": [
                "csc148",
                "CSC 236"
            ]
        }
    )

    assert response.status_code == 200