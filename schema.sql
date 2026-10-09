-- Degree Planner Database Schema 

-- ------------------------------------------------------------
-- Course
-- Stores the basic information for every course in the system.
-- ------------------------------------------------------------
CREATE TABLE Course (
    course_code VARCHAR(10) PRIMARY KEY,
    course_name TEXT NOT NULL,
    credits NUMERIC(3,1) NOT NULL,
    level INTEGER NOT NULL
);


-- ------------------------------------------------------------
-- Program
-- Stores each supported academic program, such as:
-- "Computer Science Major" or "Physics Minor".
-- ------------------------------------------------------------
CREATE TABLE Program (
    program_id SERIAL PRIMARY KEY,
    program_name TEXT UNIQUE NOT NULL
);


-- ------------------------------------------------------------
-- Prerequisite
-- Represents prerequisite relationships between courses.
-- Each row means that prerequisite_code must be completed
-- before taking course_code.
--
-- Example:
-- CSC263 | CSC236
-- means CSC236 is a prerequisite for CSC263.
-- ------------------------------------------------------------
CREATE TABLE Prerequisite (
    course_code VARCHAR(10) NOT NULL,
    prerequisite_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (course_code, prerequisite_code),

    FOREIGN KEY (course_code)
        REFERENCES Course(course_code),

    FOREIGN KEY (prerequisite_code)
        REFERENCES Course(course_code)
);


-- ------------------------------------------------------------
-- ProgramRequiredCourse
-- Stores courses that are specifically required for a program.
--
-- Example:
-- program_id 1 | CSC236
-- means CSC236 is mandatory for program 1.
-- ------------------------------------------------------------
CREATE TABLE ProgramRequiredCourse (
    program_id INTEGER NOT NULL,
    course_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (program_id, course_code),

    FOREIGN KEY (program_id)
        REFERENCES Program(program_id),

    FOREIGN KEY (course_code)
        REFERENCES Course(course_code)
);


-- ------------------------------------------------------------
-- LevelRequirement
-- Stores requirements based on course level.
--
-- Example:
-- program_id 1 | level 300 | 1.5 credits
-- means the program requires 1.5 credits at the 300 level.
-- ------------------------------------------------------------
CREATE TABLE LevelRequirement (
    program_id INTEGER NOT NULL,
    level INTEGER NOT NULL,
    required_credits NUMERIC(3,1) NOT NULL,

    PRIMARY KEY (program_id, level),

    FOREIGN KEY (program_id)
        REFERENCES Program(program_id)
);


-- ------------------------------------------------------------
-- CourseGroup
-- Represents a requirement where a student must complete
-- a certain number of credits from a specific group of courses.
--
-- Example:
-- "Upper Year Options" requiring 1.0 credits.
-- ------------------------------------------------------------
CREATE TABLE CourseGroup (
    group_id SERIAL PRIMARY KEY,
    program_id INTEGER NOT NULL,
    group_name TEXT NOT NULL,
    required_credits NUMERIC(3,1) NOT NULL,

    FOREIGN KEY (program_id)
        REFERENCES Program(program_id)
);


-- ------------------------------------------------------------
-- CourseGroupOption
-- Stores the courses that belong to each CourseGroup.
--
-- Example:
-- group_id 1 | CSC343
-- means CSC343 can count toward course group 1.
-- ------------------------------------------------------------
CREATE TABLE CourseGroupOption (
    group_id INTEGER NOT NULL,
    course_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (group_id, course_code),

    FOREIGN KEY (group_id)
        REFERENCES CourseGroup(group_id),

    FOREIGN KEY (course_code)
        REFERENCES Course(course_code)
);