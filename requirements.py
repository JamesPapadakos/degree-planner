def show_requirements(
        completed_courses, 
        required_courses, 
        courses
        ):
    print("\nCompleted courses:")

    for course in required_courses: 
        if course in completed_courses:
            print("Completed", course, "-", courses[course])

    print("\nMissing requirements:")
    for course in required_courses:
        if course not in completed_courses:
            print("Missing", course, "-", courses[course])

def show_course_eligibility(completed_courses, prerequisites):
    print("\nCourse eligibility:")
    for course in prerequisites:
        required_prereqs = prerequisites[course]

        eligible = True

        for prereq in required_prereqs:
            if prereq not in completed_courses:
                eligible = False

        if eligible:
            print("You are eligible for", course)
        else:
            print("You are not eligible for", course)

def check_level_credits(completed_courses, 
                        courses, 
                        level, 
                        required_credits
                        ):
    total_credits = 0
    for course in completed_courses:
        if course in courses:
            if courses[course]["level"] == level:
                total_credits += courses[course]["credits"]

    if total_credits >= required_credits:
        print(f"\nYou have completed enough credits for {level}-level courses.")
    else:
        credits_needed = required_credits - total_credits
        print(f"\nYou have not completed enough credits for {level}-level courses.")
        print(f"You need {credits_needed} more credits out of {required_credits}.")

def check_course_group(
        completed_courses, 
        courses, 
        group_name,
        course_options, 
        required_credits
        ): 
    total_credits = 0
    for course in completed_courses:
        if course in course_options:
            total_credits += courses[course]["credits"]

    print(f"\nCompleted credits from {group_name}: {total_credits} out of {required_credits}.")
    if total_credits >= required_credits:
        print("Requirement completed.")
    else:
        credits_needed = required_credits - total_credits
        print(f"You need {credits_needed} more credits from the course group.")

def check_program_requirements(
        completed_courses, 
        program_requirements, 
        courses 
        ):

    show_requirements(
        completed_courses, 
        program_requirements["required_courses"], 
        courses
        )
    
    for requirement in program_requirements["level_requirements"]:
        check_level_credits(
            completed_courses, 
            courses, 
            requirement["level"],
              requirement["credits"]
              )
    
    for course_group in program_requirements["course_groups"]:
        check_course_group(
            completed_courses,
            courses,
            course_group["name"],
            course_group["courses"],
            course_group["credits"])

def evaluate_program_requirements(
    completed_courses,
    courses,
    program_requirements
):
    required_results = []

    for course in program_requirements["required_courses"]:
        required_results.append({
            "course": course,
            "completed": course in completed_courses
        })

    level_results = []

    for requirement in program_requirements["level_requirements"]:
        level = requirement["level"]
        required_credits = requirement["credits"]

        total_credits = 0

        for course in completed_courses:
            if course in courses:
                if courses[course]["level"] == level:
                    total_credits += courses[course]["credits"]

        level_results.append({
            "level": level,
            "completed_credits": total_credits,
            "required_credits": required_credits,
            "remaining_credits": max(0, required_credits - total_credits),
            "completed": total_credits >= required_credits
        })

    course_group_results = []

    for group in program_requirements["course_groups"]:
        total_credits = 0

        for course in completed_courses:
            if course in group["courses"] and course in courses:
                total_credits += courses[course]["credits"]

        course_group_results.append({
            "name": group["name"],
            "completed_credits": total_credits,
            "required_credits": group["credits"],
            "remaining_credits": max(0, group["credits"] - total_credits),
            "completed": total_credits >= group["credits"]
        })

    return {
        "required_courses": required_results,
        "level_requirements": level_results,
        "course_groups": course_group_results
    }