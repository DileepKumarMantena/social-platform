import React, { useEffect, useState } from "react";
import { getChannels, getCampaigns, getLeads } from "../AppUtils";

const SECTIONS = [
  { id: "channels", label: "Channels", desc: "Connect Facebook, Instagram, LinkedIn & more", icon: "◆", color: "#7c3aed" },
  { id: "campaigns", label: "Campaigns", desc: "Create and manage campaigns", icon: "◇", color: "#0891b2" },
  { id: "leads", label: "Leads", desc: "Track and follow up on leads", icon: "●", color: "#059669" },
];

export default function Dashboard({ token, user, onNavigate }) {
  const [stats, setStats] = useState({ channels: 0, campaigns: 0, leads: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [channels, campaigns, leads] = await Promise.all([
          getChannels(token),
          getCampaigns(token),
          getLeads(token),
        ]);
        const connectedChannels = (channels || []).filter((c) => c.connected || c.active).length;
        setStats({
          channels: connectedChannels,
          campaigns: (campaigns || []).length,
          leads: (leads || []).length,
        });
      } catch {
        setStats({ channels: 0, campaigns: 0, leads: 0 });
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, [token]);

  return (
    <div className="dashboard">
      <header className="page-header">
        <h2>Dashboard</h2>
        <p className="page-subtitle">Welcome back, {user?.username || "User"}. Select a section to get started.</p>
      </header>
      <div className="metrics-bar">
        <div className="metric-card">
          <span className="metric-value">{loading ? "—" : stats.channels}</span>
          <span className="metric-label">Channels Connected</span>
        </div>
        <div className="metric-card">
          <span className="metric-value">{loading ? "—" : stats.campaigns}</span>
          <span className="metric-label">Campaigns</span>
        </div>
        <div className="metric-card">
          <span className="metric-value">{loading ? "—" : stats.leads}</span>
          <span className="metric-label">Leads</span>
        </div>
      </div>
      <div className="chart-placeholder">
        <h4>Campaign Performance</h4>
        <div className="chart-bar" style={{ width: "60%" }}><span>Last 30 days</span></div>
        <p className="chart-hint">Connect channels and run campaigns to see analytics</p>
      </div>
      <div className="nav-cards">
        {SECTIONS.map((s) => (
          <button key={s.id} type="button" className="nav-card" onClick={() => onNavigate?.(s.id)}>
            <span className="nav-card-icon" style={{ color: s.color }}>{s.icon}</span>
            <h3 className="nav-card-title">{s.label}</h3>
            <p className="nav-card-desc">{s.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
