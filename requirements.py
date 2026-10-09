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