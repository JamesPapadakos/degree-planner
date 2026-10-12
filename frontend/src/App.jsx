import { useEffect, useState } from "react";

function App() {
  const [programs, setPrograms] = useState({});
  const [selectedProgram, setSelectedProgram] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/programs")
      .then((response) => response.json())
      .then((data) => setPrograms(data));
  }, []);

  return (
    <div>
      <h1>U of T Degree Planner</h1>

      <label htmlFor="program">Program:</label>

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
    </div>
  );
}

export default App;