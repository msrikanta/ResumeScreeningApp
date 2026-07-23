import { BrowserRouter as Router, Routes, Route, Navigate, Link } from "react-router-dom";
import "./App.css";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Recruiter from "./pages/Recruiter";

function getStoredUser() {
  try {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function Navbar() {
  const token = localStorage.getItem("token");
  const storedRole = localStorage.getItem("role");
  const user = getStoredUser();

  const role = storedRole || user?.role || null;

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("username");
    localStorage.removeItem("user");
    window.location.href = "/login";
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h2 className="logo">Resume Screening System</h2>
      </div>

      <div className="navbar-right">
        {!token ? (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="nav-link">Register</Link>
          </>
        ) : (
          <>
            {role === "recruiter" ? (
              <Link to="/recruiter" className="nav-link">Recruiter Dashboard</Link>
            ) : (
              <Link to="/dashboard" className="nav-link">Candidate Dashboard</Link>
            )}
            <button className="logout-btn" onClick={handleLogout}>Logout</button>
          </>
        )}
      </div>
    </nav>
  );
}

function ProtectedRoute({ children, allowedRole = null }) {
  const token = localStorage.getItem("token");
  const storedRole = localStorage.getItem("role");
  const user = getStoredUser();

  const role = storedRole || user?.role || null;

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRole && role !== allowedRole) {
    return <Navigate to="/" replace />;
  }

  return children;
}

function HomeRedirect() {
  const token = localStorage.getItem("token");
  const storedRole = localStorage.getItem("role");
  const user = getStoredUser();

  const role = storedRole || user?.role || null;

  if (!token) return <Navigate to="/login" replace />;
  if (role === "recruiter") return <Navigate to="/recruiter" replace />;
  return <Navigate to="/dashboard" replace />;
}

function App() {
  return (
    <Router>
      <div className="app-shell">
        <Navbar />

        <main className="page-container">
          <Routes>
            <Route path="/" element={<HomeRedirect />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute allowedRole="candidate">
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/recruiter"
              element={
                <ProtectedRoute allowedRole="recruiter">
                  <Recruiter />
                </ProtectedRoute>
              }
            />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;