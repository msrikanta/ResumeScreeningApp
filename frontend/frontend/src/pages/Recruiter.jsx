import { useEffect, useState } from "react";
import { getRecruiterResumes } from "../api";
import ResumeList from "../components/ResumeList";

function Recruiter() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const fetchResumes = async () => {
    try {
      setLoading(true);
      setMessage("");

      const token = localStorage.getItem("token");
      if (!token) {
        setMessage("No token found. Please login again.");
        return;
      }

      const data = await getRecruiterResumes(token);
      console.log("Recruiter resumes response:", data);

      if (Array.isArray(data)) {
        setResumes(data);
        if (data.length === 0) {
          setMessage("No resumes found.");
        }
      } else {
        setResumes([]);
        setMessage("Unexpected recruiter response format.");
      }
    } catch (error) {
      console.error("Recruiter fetch error:", error);
      setMessage(error.response?.data?.detail || "Failed to fetch resumes.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  return (
    <div className="dashboard-container">
      <div className="card dashboard-card">
        <h2>Recruiter Dashboard</h2>
        <p>View all uploaded resumes and ATS scores.</p>

        <button className="secondary-btn" onClick={fetchResumes}>
          Refresh
        </button>
      </div>

      <div className="card">
        {loading ? (
          <p>Loading resumes...</p>
        ) : message && resumes.length === 0 ? (
          <p className="status-message">{message}</p>
        ) : (
          <ResumeList resumes={resumes} />
        )}
      </div>
    </div>
  );
}

export default Recruiter;