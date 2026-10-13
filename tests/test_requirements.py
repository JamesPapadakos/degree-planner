from requirements import evaluate_program_requirements

courses = {
    "CSC148": {
        "name": "Introduction to Computer Science",
        "credits": 0.5,
        "level": 100
    },
    "CSC236": {
        "name": "Introduction to the Theory of Computation",
        "credits": 0.5,
        "level": 200
    },
    "CSC343": {
        "name": "Introduction to Databases",
        "credits": 0.5,
        "level": 300
    },
    "CSC369": {
        "name": "Operating Systems",
        "credits": 0.5,
        "level": 300
    }
}

program_requirements = {
    "required_courses": [
        "CSC236"
    ],
    "level_requirements": [
        {
            "level": 300,
            "credits": 1.0
        }
    ],
    "course_groups": [
        {
            "name": "Upper Year Options",
            "courses": [
                "CSC343",
                "CSC369"
            ],
            "credits": 0.5
        }
    ]
}

def test_required_course_completed():
    completed_courses = [
        "CSC236",
        "CSC343"
    ]

    results = evaluate_program_requirements(
        completed_courses,
        courses,
        program_requirements
    )

    assert results["required_courses"][0]["completed"] is True

def test_required_course_missing():
    completed_courses = [
        "CSC343"
    ]

    results = evaluate_program_requirements(
        completed_courses,
        courses,
        program_requirements
    )

    assert results["required_courses"][0]["completed"] is False

def test_level_requirement_completed():
    completed_courses = [
        "CSC343",
        "CSC369"
    ]

    results = evaluate_program_requirements(
        completed_courses,
        courses,
        program_requirements
    )

    level_result = results["level_requirements"][0]

    assert level_result["completed_credits"] == 1.0
    assert level_result["completed"] is True

def test_level_requirement_incomplete():
    completed_courses = [
        "CSC343"
    ]

    results = evaluate_program_requirements(
        completed_courses,
        courses,
        program_requirements
    )

    level_result = results["level_requirements"][0]

    assert level_result["completed_credits"] == 0.5
    assert level_result["completed"] is False

def test_course_group_completed():
    completed_courses = [
        "CSC343"
    ]

    results = evaluate_program_requirements(
        completed_courses,
        courses,
        program_requirements
    )

    group_result = results["course_groups"][0]

    assert group_result["completed_credits"] == 0.5
    assert group_result["completed"] is True

def test_no_completed_courses():
    completed_courses = []

    results = evaluate_program_requirements(
        completed_courses,
        courses,
        program_requirements
    )

    assert results["required_courses"][0]["completed"] is False
    assert results["level_requirements"][0]["completed_credits"] == 0
    assert results["level_requirements"][0]["completed"] is False
    assert results["course_groups"][0]["completed_credits"] == 0
    assert results["course_groups"][0]["completed"] is False