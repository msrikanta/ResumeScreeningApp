import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [token, setToken] = useState(localStorage.getItem("token"));
  const [role, setRole] = useState(localStorage.getItem("role"));

  useEffect(() => {
    setToken(localStorage.getItem("token"));
    setRole(localStorage.getItem("role"));
  }, [location]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("username");
    localStorage.removeItem("user");

    setToken(null);
    setRole(null);

    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h2 className="logo">Resume Screening System</h2>
      </div>

      <div className="navbar-right">
        {!token ? (
          <>
            <Link to="/register" className="nav-link">
              Register
            </Link>

            <Link to="/login" className="nav-link">
              Login
            </Link>
          </>
        ) : (
          <>
            {role === "candidate" && (
              <Link to="/dashboard" className="nav-link">
                Dashboard
              </Link>
            )}

            {role === "recruiter" && (
              <Link to="/recruiter" className="nav-link">
                Recruiter
              </Link>
            )}

            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;