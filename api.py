from fastapi import FastAPI, HTTPException
from database import (
    load_courses, 
    load_programs,
    load_program_requirements
)
from requirements import evaluate_program_requirements
from pydantic import BaseModel

app = FastAPI()

class DegreeCheckRequest(BaseModel):
    program_id: int
    completed_courses: list[str]

def normalize_course_code(course):
    return course.replace(" ", "").upper()

@app.get("/")
def root():
    return {"message": "Degree Planner API is running"}

@app.get("/courses")
def get_courses():
    return load_courses()

@app.get("/programs")
def get_programs():
    return load_programs()

@app.get("/programs/{program_id}")
def get_program_requirements(program_id: int):
    return load_program_requirements(program_id)

@app.post("/degree-check")
def degree_check(request: DegreeCheckRequest):
    courses = load_courses()
    programs = load_programs()

    if request.program_id not in programs.values():
        raise HTTPException(status_code=404, detail="Program not found")

    normalized_courses = []
    for course in request.completed_courses:
        normalized_course = normalize_course_code(course)

        if normalized_course not in normalized_courses:
            normalized_courses.append(normalized_course)

    invalid_courses = []
    for course in normalized_courses:
        if course not in courses:
            invalid_courses.append(course)

    if invalid_courses:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid course codes: {', '.join(invalid_courses)}"
        )

    program_requirements = load_program_requirements(request.program_id)

    results = evaluate_program_requirements(
        normalized_courses,
        courses,
        program_requirements
    )

    return {
    "program_id": request.program_id,
    "required_courses": results["required_courses"],
    "level_requirements": results["level_requirements"],
    "course_groups": results["course_groups"]
    }
