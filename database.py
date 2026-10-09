import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        dbname="degree_planner",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )


def load_courses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT course_code, course_name, credits, level
        FROM Course;
    """)

    rows = cursor.fetchall()

    courses = {}

    for course_code, course_name, credits, level in rows:
        courses[course_code] = {
            "name": course_name,
            "credits": float(credits),
            "level": level
        }

    cursor.close()
    connection.close()

    return courses


def load_prerequisites():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT course_code, prerequisite_code
        FROM Prerequisite;
    """)

    rows = cursor.fetchall()

    prerequisites = {}

    for course_code, prerequisite_code in rows:
        if course_code not in prerequisites:
            prerequisites[course_code] = []

        prerequisites[course_code].append(prerequisite_code)

    cursor.close()
    connection.close()

    return prerequisites


def load_programs():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT program_id, program_name
        FROM Program;
    """)

    rows = cursor.fetchall()

    programs = {}

    for program_id, program_name in rows:
        programs[program_name] = program_id

    cursor.close()
    connection.close()

    return programs

def load_required_courses(program_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT course_code
        FROM ProgramRequiredCourse
        WHERE program_id = %s;
    """, (program_id,))

    rows = cursor.fetchall()

    required_courses = []

    for row in rows:
        required_courses.append(row[0])

    cursor.close()
    connection.close()

    return required_courses

def load_level_requirements(program_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT level, required_credits
        FROM LevelRequirement
        WHERE program_id = %s;
    """, (program_id,))

    rows = cursor.fetchall()

    level_requirements = []

    for level, required_credits in rows:
        level_requirements.append({
            "level": level,
            "credits": float(required_credits)
        })

    cursor.close()
    connection.close()

    return level_requirements

def load_course_groups(program_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT group_id, group_name, required_credits
        FROM CourseGroup
        WHERE program_id = %s;
    """, (program_id,))

    group_rows = cursor.fetchall()

    course_groups = []

    for group_id, group_name, required_credits in group_rows:
        cursor.execute("""
            SELECT course_code
            FROM CourseGroupOption
            WHERE group_id = %s;
        """, (group_id,))

        option_rows = cursor.fetchall()

        course_options = []

        for row in option_rows:
            course_options.append(row[0])

        course_groups.append({
            "name": group_name,
            "courses": course_options,
            "credits": float(required_credits)
        })

    cursor.close()
    connection.close()

    return course_groups

def load_program_requirements(program_id):
    return {
        "required_courses": load_required_courses(program_id),
        "level_requirements": load_level_requirements(program_id),
        "course_groups": load_course_groups(program_id)
    }
