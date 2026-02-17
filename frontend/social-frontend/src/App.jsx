// App.jsx
import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import Channels from "./components/Channels";
import Campaigns from "./components/Campaigns";
import Leads from "./components/Leads";
import Settings from "./components/Settings";
import "./App.css";

const THEME_KEY = "socialmark-theme";
const VIEWS = { dashboard: "dashboard", channels: "channels", campaigns: "campaigns", leads: "leads", settings: "settings" };

function App() {
  const [auth, setAuth] = useState(null);
  const [view, setView] = useState(VIEWS.dashboard);
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_KEY) || "dark");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  const token = auth?.token;
  const user = auth?.user || { username: token, tenant_name: "Demo", role: "user" };

  if (!token) return <Login setAuth={setAuth} />;

  const handleLogout = () => setAuth(null);

  const renderContent = () => {
    switch (view) {
      case VIEWS.channels:
        return <Channels token={token} user={user} />;
      case VIEWS.campaigns:
        return <Campaigns token={token} user={user} />;
      case VIEWS.leads:
        return <Leads token={token} user={user} />;
      case VIEWS.settings:
        return <Settings token={token} user={user} theme={theme} onThemeChange={setTheme} />;
      default:
        return <Dashboard token={token} user={user} onNavigate={setView} />;
    }
  };

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
            className={`nav-btn ${view === VIEWS.dashboard ? "active" : ""}`}
            onClick={() => setView(VIEWS.dashboard)}
          >
            <span className="nav-icon">◉</span>
            Dashboard
          </button>
          <button
            type="button"
            className={`nav-btn ${view === VIEWS.channels ? "active" : ""}`}
            onClick={() => setView(VIEWS.channels)}
          >
            <span className="nav-icon">◆</span>
            Channels
          </button>
          <button
            type="button"
            className={`nav-btn ${view === VIEWS.campaigns ? "active" : ""}`}
            onClick={() => setView(VIEWS.campaigns)}
          >
            <span className="nav-icon">◇</span>
            Campaigns
          </button>
          <button
            type="button"
            className={`nav-btn ${view === VIEWS.leads ? "active" : ""}`}
            onClick={() => setView(VIEWS.leads)}
          >
            <span className="nav-icon">●</span>
            Leads
          </button>
          <button
            type="button"
            className={`nav-btn ${view === VIEWS.settings ? "active" : ""}`}
            onClick={() => setView(VIEWS.settings)}
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
      <main className="main-content">{renderContent()}</main>
    </div>
  );
}

export default App;
