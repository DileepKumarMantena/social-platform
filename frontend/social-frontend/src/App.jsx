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
  const [token, setToken] = useState(null);
  const [view, setView] = useState(VIEWS.dashboard);

  if (!token) return <Login setToken={setToken} />;

  const handleLogout = () => setToken(null);

  const renderContent = () => {
    switch (view) {
      case VIEWS.channels:
        return <Channels token={token} />;
      case VIEWS.campaigns:
        return <Campaigns token={token} />;
      case VIEWS.leads:
        return <Leads token={token} />;
      default:
        return <Dashboard token={token} onNavigate={setView} />;
    }
  };

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="sidebar-title">Social</h1>
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
