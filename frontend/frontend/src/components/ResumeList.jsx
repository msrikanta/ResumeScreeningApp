function ResumeList({ resumes }) {
  if (!resumes || resumes.length === 0) {
    return <p className="muted">No resumes uploaded yet.</p>;
  }

  return (
    <div className="resume-table-wrapper">
      <table className="resume-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>File Name</th>
            <th>Job Title</th>
            <th>ATS Score</th>
            <th>Uploaded At</th>
            <th>User ID</th>
          </tr>
        </thead>
        <tbody>
          {resumes.map((resume) => (
            <tr key={resume.id}>
              <td>{resume.id}</td>
              <td>{resume.file_name}</td>
              <td>{resume.job_title || "-"}</td>
              <td>
                <span className="score-pill">{resume.score}%</span>
              </td>
              <td>{new Date(resume.uploaded_at).toLocaleString()}</td>
              <td>{resume.user_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResumeList;