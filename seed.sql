-- Degree Planner Seed Data

-- ------------------------------------------------------------
-- Courses
-- ------------------------------------------------------------
INSERT INTO Course (
    course_code,
    course_name,
    credits,
    level
)
VALUES
    ('CSC148', 'Introduction to Computer Science', 0.5, 100),
    ('CSC236', 'Introduction to the Theory of Computation', 0.5, 200),
    ('CSC263', 'Data Structures and Analysis', 0.5, 200),
    ('CSC343', 'Introduction to Databases', 0.5, 300),
    ('CSC369', 'Operating Systems', 0.5, 300),
    ('CSC373', 'Algorithm Design, Analysis & Complexity', 0.5, 300),
    ('CSC384', 'Introduction to Artificial Intelligence', 0.5, 300);


-- ------------------------------------------------------------
-- Programs
-- ------------------------------------------------------------
INSERT INTO Program (program_name)
VALUES
    ('Computer Science Major'),
    ('Physics Minor');


-- ------------------------------------------------------------
-- Prerequisites
-- ------------------------------------------------------------
INSERT INTO Prerequisite (
    course_code,
    prerequisite_code
)
VALUES
    ('CSC236', 'CSC148'),
    ('CSC263', 'CSC236');


-- ------------------------------------------------------------
-- Required courses for the Computer Science Major
-- Assumes Computer Science Major receives program_id = 1.
-- ------------------------------------------------------------
INSERT INTO ProgramRequiredCourse (
    program_id,
    course_code
)
VALUES
    (1, 'CSC236'),
    (1, 'CSC263');


-- ------------------------------------------------------------
-- Course-level credit requirements
-- ------------------------------------------------------------
INSERT INTO LevelRequirement (
    program_id,
    level,
    required_credits
)
VALUES
    (1, 300, 1.5),
    (1, 400, 2.0);


-- ------------------------------------------------------------
-- Course groups
-- ------------------------------------------------------------
INSERT INTO CourseGroup (
    program_id,
    group_name,
    required_credits
)
VALUES
    (1, 'Upper Year Options', 1.0);


-- ------------------------------------------------------------
-- Courses that satisfy the Upper Year Options group
-- Assumes the group above receives group_id = 1.
-- ------------------------------------------------------------
INSERT INTO CourseGroupOption (
    group_id,
    course_code
)
VALUES
    (1, 'CSC343'),
    (1, 'CSC369'),
    (1, 'CSC373'),
    (1, 'CSC384');