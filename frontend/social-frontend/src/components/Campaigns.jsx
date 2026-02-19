import React, { useEffect, useState } from "react";
import "./Campaigns.css";

const CHANNEL_COLORS = {
  facebook: "#1877f2",
  instagram: "#e4405f",
  linkedin: "#0a66c2",
  twitter: "#1da1f2",
  youtube: "#ff0000",
  "google-ads": "#4285f4",
};

export default function Campaigns({ token, user }) {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const canEdit = user?.role === "admin" || user?.role === "lead";

  const dummyCampaigns = [
    {
      id: 1,
      name: "Summer Sale 2024",
      channel_name: "Facebook",
      channel_slug: "facebook",
      budget: 5000,
      status: "active",
      impressions: 245000,
      clicks: 8200,
      engagement: 3.4,
      created_at: "2024-01-15",
    },
    {
      id: 2,
      name: "Product Launch",
      channel_name: "Instagram",
      channel_slug: "instagram",
      budget: 3000,
      status: "pending",
      impressions: 189000,
      clicks: 6700,
      engagement: 3.5,
      created_at: "2024-01-20",
    },
    {
      id: 3,
      name: "Brand Awareness",
      channel_name: "LinkedIn",
      channel_slug: "linkedin",
      budget: 2000,
      status: "draft",
      impressions: 98000,
      clicks: 2100,
      engagement: 2.1,
      created_at: "2024-02-01",
    },
    {
      id: 4,
      name: "Holiday Special",
      channel_name: "Twitter",
      channel_slug: "twitter",
      budget: 4500,
      status: "active",
      impressions: 512000,
      clicks: 15600,
      engagement: 3.0,
      created_at: "2024-02-10",
    },
    {
      id: 5,
      name: "Q1 Promotion",
      channel_name: "Google Ads",
      channel_slug: "google-ads",
      budget: 3500,
      status: "active",
      impressions: 67000,
      clicks: 3400,
      engagement: 5.1,
      created_at: "2024-01-05",
    },
  ];

  useEffect(() => {
    setLoading(false);
    setCampaigns(dummyCampaigns);
  }, []);

  const handleCreateCampaign = (e) => {
    e.preventDefault();
    setError("");
    const formData = new FormData(e.target);
    const channel = formData.get("channel");
    
    if (!channel || !formData.get("name") || !formData.get("budget")) {
      setError("Please fill in all required fields");
      return;
    }
    
    const newCampaign = {
      id: campaigns.length + 1,
      name: formData.get("name"),
      channel_name: channel.charAt(0).toUpperCase() + channel.slice(1),
      channel_slug: channel,
      budget: parseFloat(formData.get("budget")),
      status: "draft",
      impressions: 0,
      clicks: 0,
      engagement: 0,
      created_at: new Date().toISOString().split('T')[0],
    };
    
    setCampaigns([...campaigns, newCampaign]);
    setShowForm(false);
    e.target.reset();
  };

  const handleViewResults = (campaign) => {
    setSelectedCampaign(campaign);
  };

  const handleStatusChange = (campaignId, newStatus) => {
    setCampaigns(campaigns.map(campaign => 
      campaign.id === campaignId 
        ? { ...campaign, status: newStatus }
        : campaign
    ));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "active": return "#10b981";
      case "pending": return "#f59e0b";
      case "completed": return "#6b7280";
      default: return "#6b7280";
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "active": return "🟢";
      case "pending": return "🟡";
      case "completed": return "⚪";
      default: return "⚪";
    }
  };

  if (loading) {
    return (
      <div className="data-section">
        <div className="loading-state">Loading campaigns...</div>
      </div>
    );
  }

  return (
    <div className="campaigns">
      <header className="page-header page-header-row">
        <div>
          <h2>🚀 Campaigns</h2>
          <p className="page-subtitle">Create and manage your marketing campaigns</p>
        </div>
        {canEdit && (
          <button type="button" className="btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? "Cancel" : "➕ Add Campaign"}
          </button>
        )}
      </header>

      {showForm && (
        <form onSubmit={handleCreateCampaign} className="campaign-form" style={{ marginBottom: "1.5rem" }}>
          {error && <div className="campaigns-error-message" style={{ marginBottom: "1rem", color: "#d32f2f" }}>{error}</div>}
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="camp-name">Campaign Name</label>
              <input
                id="camp-name"
                name="name"
                type="text"
                placeholder="Enter campaign name"
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="camp-channel">Channel</label>
              <select id="camp-channel" name="channel" className="form-select">
                <option value="">Select channel</option>
                <option value="facebook">📘 Facebook</option>
                <option value="instagram">📷 Instagram</option>
                <option value="linkedin">💼 LinkedIn</option>
                <option value="twitter">🐦 Twitter</option>
                <option value="google-ads">🔍 Google Ads</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="camp-budget">Budget ($)</label>
              <input
                id="camp-budget"
                name="budget"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                className="form-input"
              />
            </div>
          </div>
          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setShowForm(false)}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              ✨ Create Campaign
            </button>
          </div>
        </form>
      )}
      <div className="campaigns-grid">
        {campaigns.map((campaign) => {
          const color = CHANNEL_COLORS[campaign.channel_slug] || "#6366f1";
          return (
            <div key={campaign.id} className="campaign-card">
              <div className="campaign-header">
                <div className="campaign-info">
                  <h3 className="campaign-name">{campaign.name}</h3>
                  <div className="campaign-channel" style={{ borderColor: color }}>
                    <span className="channel-icon">
                      {campaign.channel_slug === "facebook" && "📘"}
                      {campaign.channel_slug === "instagram" && "📷"}
                      {campaign.channel_slug === "linkedin" && "💼"}
                      {campaign.channel_slug === "twitter" && "🐦"}
                      {campaign.channel_slug === "google-ads" && "�"}
                    </span>
                    {campaign.channel_name}
                  </div>
                  <div className="campaign-budget">${campaign.budget.toLocaleString()}</div>
                </div>
                <div className="campaign-status">
                  {canEdit ? (
                    <select 
                      value={campaign.status || "draft"} 
                      onChange={(e) => handleStatusChange(campaign.id, e.target.value)}
                      className="status-select"
                      style={{ 
                        backgroundColor: getStatusColor(campaign.status),
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        padding: '4px 8px',
                        fontSize: '0.8rem'
                      }}
                    >
                      <option value="draft">📝 Draft</option>
                      <option value="pending">⏳ Pending</option>
                      <option value="active">🟢 Active</option>
                      <option value="completed">✅ Completed</option>
                    </select>
                  ) : (
                    <span className={`status-badge status-${campaign.status || "draft"}`} style={{ backgroundColor: getStatusColor(campaign.status) }}>
                      {campaign.status || "draft"}
                    </span>
                  )}
                </div>
              </div>
              <div className="campaign-actions">
                <button className="btn-secondary" onClick={() => handleViewResults(campaign)}>
                  View Results
                </button>
                {canEdit && (
                  <button className="btn-primary" onClick={() => setShowForm(true)}>
                    Edit Campaign
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {selectedCampaign && (
        <div className="modal-overlay" onClick={() => setSelectedCampaign(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📊 Campaign Analytics</h3>
              <button className="modal-close" onClick={() => setSelectedCampaign(null)}>✕</button>
            </div>
            <div className="modal-body">
              <div className="analytics-summary">
                <div className="summary-card">
                  <h4>{selectedCampaign.name}</h4>
                  <p className="summary-channel">{selectedCampaign.channel_name}</p>
                </div>
                <div className="summary-metrics">
                  <div className="summary-metric">
                    <span className="summary-value">{selectedCampaign.impressions.toLocaleString()}</span>
                    <span className="summary-label">Impressions</span>
                  </div>
                  <div className="summary-metric">
                    <span className="summary-value">{selectedCampaign.clicks.toLocaleString()}</span>
                    <span className="summary-label">Clicks</span>
                  </div>
                  <div className="summary-metric">
                    <span className="summary-value">{selectedCampaign.engagement}%</span>
                    <span className="summary-label">Engagement</span>
                  </div>
                </div>
              </div>
              <div className="analytics-details">
                <div className="detail-row">
                  <span className="detail-label">Budget Used:</span>
                  <span className="detail-value">${(selectedCampaign.budget * 0.75).toLocaleString()} / ${selectedCampaign.budget.toLocaleString()}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Cost per Click:</span>
                  <span className="detail-value">${(selectedCampaign.budget / selectedCampaign.clicks).toFixed(2)}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Conversion Rate:</span>
                  <span className="detail-value">{(selectedCampaign.engagement * 0.3).toFixed(1)}%</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Start Date:</span>
                  <span className="detail-value">{new Date(selectedCampaign.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
