import React from "react";

const SECTIONS = [
  { id: "channels", label: "Channels", desc: "Manage your marketing channels", icon: "◆", color: "#7c3aed" },
  { id: "campaigns", label: "Campaigns", desc: "View and manage campaigns", icon: "◇", color: "#0891b2" },
  { id: "leads", label: "Leads", desc: "Browse and track leads", icon: "●", color: "#059669" },
];

export default function Dashboard({ token, onNavigate }) {
  return (
    <div className="dashboard">
      <header className="page-header">
        <h2>Dashboard</h2>
        <p className="page-subtitle">Welcome back. Select a section to get started.</p>
      </header>
      <div className="info-card" style={{ marginBottom: "24px" }}>
        <div className="info-row">
          <span className="info-label">Status</span>
          <span className="status-badge">Logged in</span>
        </div>
        <div className="info-row">
          <span className="info-label">Session</span>
          <code className="token-preview">{token?.slice(0, 20)}...</code>
        </div>
      </div>
      <div className="nav-cards">
        {SECTIONS.map((s) => (
          <button
            key={s.id}
            type="button"
            className="nav-card"
            onClick={() => onNavigate?.(s.id)}
          >
            <span className="nav-card-icon" style={{ color: s.color }}>{s.icon}</span>
            <h3 className="nav-card-title">{s.label}</h3>
            <p className="nav-card-desc">{s.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
