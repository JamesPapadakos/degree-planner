from database import (
    load_courses,
    load_prerequisites,
    load_programs,
    load_program_requirements
)

from requirements import (
    check_program_requirements,
    show_course_eligibility
)

def get_completed_courses():
    completed_courses_input = input("Enter completed courses (comma-separated): ")
    completed_courses = []
    for course in completed_courses_input.split(","):
        completed_courses.append(course.strip().upper())
    return completed_courses

def get_program_choice():
    print("Available programs:")
    for program in programs:
        print("-", program)
    selected_program = input("Enter the program you are enrolled in: ")
    if selected_program in programs:
        return selected_program
    else:
        print("Invalid program choice. Please try again.")
        return get_program_choice()


if __name__ == "__main__":
    courses = load_courses()
    prerequisites = load_prerequisites()
    programs = load_programs()

    completed_courses = get_completed_courses()
    selected_program = get_program_choice()

    program_id = programs[selected_program]

    program_requirements = load_program_requirements(program_id)

    check_program_requirements(
        completed_courses,
        program_requirements,
        courses
    )

    show_course_eligibility(
        completed_courses,
        prerequisites
    )