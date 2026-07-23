import ResumeUpload from "../components/ResumeUpload";

function Dashboard() {
  const username = localStorage.getItem("username");

  return (
    <div className="dashboard-container">
      <div className="card dashboard-card">
        <h2>Candidate Dashboard</h2>
        <p>
          Welcome{username ? `, ${username}` : ""}!
        </p>
        <p className="muted">
          Upload your resume to get an ATS score.
        </p>
      </div>

      <ResumeUpload />
    </div>
  );
}

export default Dashboard;