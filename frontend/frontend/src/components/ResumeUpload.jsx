import { useState } from "react";
import { uploadResume } from "../api";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [message, setMessage] = useState("");
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();

    setMessage("");
    setScore(null);

    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login first.");
      return;
    }

    if (!file) {
      setMessage("Please choose a resume file.");
      return;
    }

    if (!jobTitle.trim()) {
      setMessage("Please enter a job title.");
      return;
    }

    if (!jobDescription.trim()) {
      setMessage("Please enter a job description.");
      return;
    }

    try {
      setLoading(true);

      const data = await uploadResume(file, jobTitle, jobDescription, token);

      setMessage("Resume uploaded successfully.");
      setScore(data.score ?? null);

      // reset form
      setFile(null);
      setJobTitle("");
      setJobDescription("");

      const fileInput = document.getElementById("resumeFileInput");
      if (fileInput) fileInput.value = "";
    } catch (error) {
      console.error("Upload error:", error);
      setMessage(error.response?.data?.detail || "Resume upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card upload-card">
      <h3>Upload Resume for ATS Screening</h3>
      <p className="muted">
        Enter the job details and upload a resume to calculate ATS score.
      </p>

      {message && <div className="status-message">{message}</div>}

      {score !== null && (
        <div className="score-box">
          ATS Score: <strong>{score}%</strong>
        </div>
      )}

      <form onSubmit={handleUpload} className="form-grid">
        <div className="form-group">
          <label className="form-label">Job Title</label>
          <input
            type="text"
            className="form-input"
            placeholder="e.g. Python Backend Developer"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Job Description</label>
          <textarea
            className="form-input form-textarea"
            rows="8"
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Resume File</label>
          <input
            id="resumeFileInput"
            type="file"
            className="form-input"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
          <small className="muted">
            Supported formats: PDF, DOCX
          </small>
        </div>

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? "Uploading..." : "Upload Resume"}
        </button>
      </form>
    </div>
  );
}

export default ResumeUpload;