// App.jsx
import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import Channels from "./components/Channels";
import Campaigns from "./components/Campaigns";
import Leads from "./components/Leads";
import Settings from "./components/Settings";
import Analytics from "./components/Analytics";
import CampaignScheduler from "./components/CampaignScheduler";
import "./App.css";

const THEME_KEY = "socialmark-theme";

function AppContent() {
  const [auth, setAuth] = useState(() => {
    const saved = localStorage.getItem("auth");
    return saved ? JSON.parse(saved) : null;
  });
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_KEY) || "dark");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (auth) {
      localStorage.setItem("auth", JSON.stringify(auth));
    } else {
      localStorage.removeItem("auth");
    }
  }, [auth]);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  const token = auth?.token;
  const user = auth?.user || { username: token, tenant_name: "Demo", role: "user" };

  const handleLogout = () => {
    setAuth(null);
    navigate("/login");
  };

  if (!token) {
    return (
      <Routes>
        <Route path="/login" element={<Login setAuth={setAuth} />} />
        <Route path="/register" element={<Register setAuth={setAuth} />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="sidebar-title">SocialMark</h1>
          <div className="sidebar-meta">
            <span className="tenant-badge">{user.tenant_name || "Demo"}</span>
            <span className="role-badge">{user.role || "user"}</span>
          </div>
        </div>
        <nav className="sidebar-nav">
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/" || location.pathname === "/dashboard" ? "active" : ""}`}
            onClick={() => navigate("/dashboard")}
          >
            <span className="nav-icon">◉</span>
            Dashboard
          </button>
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/channels" ? "active" : ""}`}
            onClick={() => navigate("/channels")}
          >
            <span className="nav-icon">◆</span>
            Channels
          </button>
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/campaigns" ? "active" : ""}`}
            onClick={() => navigate("/campaigns")}
          >
            <span className="nav-icon">◇</span>
            Campaigns
          </button>
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/leads" ? "active" : ""}`}
            onClick={() => navigate("/leads")}
          >
            <span className="nav-icon">●</span>
            Leads
          </button>
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/analytics" ? "active" : ""}`}
            onClick={() => navigate("/analytics")}
          >
            <span className="nav-icon">📈</span>
            Analytics
          </button>
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/scheduler" ? "active" : ""}`}
            onClick={() => navigate("/scheduler")}
          >
            <span className="nav-icon">📅</span>
            Scheduler
          </button>
          <button
            type="button"
            className={`nav-btn ${location.pathname === "/settings" ? "active" : ""}`}
            onClick={() => navigate("/settings")}
          >
            <span className="nav-icon">⚙</span>
            Settings
          </button>
        </nav>
        <div className="sidebar-footer">
          <button type="button" className="nav-btn logout-btn" onClick={handleLogout}>
            <span className="nav-icon">→</span>
            Logout
          </button>
        </div>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard token={token} user={user} onNavigate={(view) => navigate(`/${view}`)} />} />
          <Route path="/dashboard" element={<Dashboard token={token} user={user} onNavigate={(view) => navigate(`/${view}`)} />} />
          <Route path="/channels" element={<Channels token={token} user={user} />} />
          <Route path="/campaigns" element={<Campaigns token={token} user={user} />} />
          <Route path="/leads" element={<Leads token={token} user={user} />} />
          <Route path="/analytics" element={<Analytics token={token} user={user} />} />
          <Route path="/scheduler" element={<CampaignScheduler token={token} user={user} />} />
          <Route path="/settings" element={<Settings token={token} user={user} theme={theme} onThemeChange={setTheme} />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
