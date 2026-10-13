import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [programs, setPrograms] = useState({});
  const [selectedProgram, setSelectedProgram] = useState("");
  const [courses, setCourses] = useState({});
  const [completedCourses, setCompletedCourses] = useState([]);
  const [degreeResults, setDegreeResults] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [courseSearch, setCourseSearch] = useState("");

  useEffect(() => {
  fetch("http://127.0.0.1:8000/programs")
    .then((response) => response.json())
    .then((data) => setPrograms(data));

  fetch("http://127.0.0.1:8000/courses")
    .then((response) => response.json())
    .then((data) => setCourses(data));
}, []);

  function checkDegree() {
  if (!selectedProgram) {
    setErrorMessage("Please select a program.");
    return;
  }
  setErrorMessage("");
  setDegreeResults(null);

  fetch("http://127.0.0.1:8000/degree-check", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      program_id: Number(selectedProgram),
      completed_courses: completedCourses,
    }),
  })
    .then(async (response) => {
      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : data.detail?.message || "Something went wrong."
        );
      }

      return data;
    })
    .then((data) => {
      setDegreeResults(data);
    })
    .catch((error) => {
      setErrorMessage(error.message);
    });
}

  return (
  <div className="app">
      <header className="app-header">
        <h1>U of T Degree Planner</h1>
        <p>Track completed courses and check your degree progress.</p>
      </header>

      <main className="planner">
        <section className="card">
          <h2>Program</h2>

          <select
            id="program"
            value={selectedProgram}
            onChange={(event) => setSelectedProgram(event.target.value)}
          >
            <option value="">Select a program</option>

            {Object.entries(programs).map(([programName, programId]) => (
              <option key={programId} value={programId}>
                {programName}
              </option>
            ))}
          </select>
        </section>

        <section className="card">
          <h2>Completed Courses</h2>

          <input
            type="text"
            placeholder="Search courses..."
            value={courseSearch}
            onChange={(event) => setCourseSearch(event.target.value)}
          />

          <p>Selected courses: {completedCourses.length}</p>

          <div className="course-list">
            {Object.entries(courses)
              .filter(([courseCode, courseInfo]) => {
                const search = courseSearch.toLowerCase();

                return (
                  courseCode.toLowerCase().includes(search) ||
                  courseInfo.name.toLowerCase().includes(search)
                );
              })
              .map(([courseCode, courseInfo]) => (
                <div className="course-item" key={courseCode}>
                  <input
                    type="checkbox"
                    id={courseCode}
                    checked={completedCourses.includes(courseCode)}
                    onChange={(event) => {
                      if (event.target.checked) {
                        setCompletedCourses([
                          ...completedCourses,
                          courseCode,
                        ]);
                      } else {
                        setCompletedCourses(
                          completedCourses.filter(
                            (course) => course !== courseCode
                          )
                        );
                      }
                    }}
                  />

                  <label htmlFor={courseCode}>
                    <strong>{courseCode}</strong> - {courseInfo.name}
                  </label>
                </div>
              ))}
          </div>

          <button onClick={checkDegree}>
            Check Degree
          </button>

          {errorMessage && (
            <p className="error-message">
              {errorMessage}
            </p>
          )}
        </section>

        {degreeResults && (
          <section className="card">
          <h2>Degree Progress</h2>

          <h3>Required Courses</h3>

          <div className="required-course-list">
            {degreeResults.required_courses.map((requirement) => (
              <div
                className={`required-course-item ${
                  requirement.completed ? "completed" : "missing"
                }`}
                key={requirement.course}
              >
                <span className="status-icon">
                  {requirement.completed ? "✓" : "✗"}
                </span>

                <span>{requirement.course}</span>

                <span className="status-text">
                  {requirement.completed ? "Completed" : "Missing"}
                </span>
              </div>
            ))}
          </div>

          <h3>Level Requirements</h3>

          {degreeResults.level_requirements.map((requirement) => {
            const progress = Math.min(
              100,
              (requirement.completed_credits / requirement.required_credits) * 100
            );

            return (
              <div className="requirement-block" key={requirement.level}>
                <div className="requirement-header">
                  <span>{requirement.level}-level courses</span>
                  <span>
                    {requirement.completed_credits} / {requirement.required_credits} credits
                  </span>
                </div>

                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                  />
                </div>

                {!requirement.completed && (
                  <p>
                    You need {requirement.remaining_credits} more credits.
                  </p>
                )}
              </div>
            );
          })}

          <h3>Course Groups</h3>
          {degreeResults.course_groups.map((group) => {
            const progress = Math.min(
              100,
              (group.completed_credits / group.required_credits) * 100
            );

            return (
              <div className="requirement-block" key={group.name}>
                <div className="requirement-header">
                  <span>{group.name}</span>
                  <span>
                    {group.completed_credits} / {group.required_credits} credits
                  </span>
                </div>

                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                  />
                </div>

                {!group.completed && (
                  <p>
                    You need {group.remaining_credits} more credits.
                  </p>
                )}
              </div>
            );
          })}
        </section>
      )}
    </main>
  </div>
);
}

export default App;