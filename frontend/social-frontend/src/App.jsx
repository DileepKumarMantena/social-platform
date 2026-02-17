// App.jsx
import React, { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import Channels from "./components/Channels";
import Campaigns from "./components/Campaigns";
import Leads from "./components/Leads";
import "./App.css";

const VIEWS = { dashboard: "dashboard", channels: "channels", campaigns: "campaigns", leads: "leads" };

function App() {
  const [auth, setAuth] = useState(null);
  const [view, setView] = useState(VIEWS.dashboard);

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
