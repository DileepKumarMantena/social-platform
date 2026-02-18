import React, { useState, useEffect } from "react";
import "./CampaignScheduler.css";

export default function CampaignScheduler({ token, user }) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [campaigns, setCampaigns] = useState([]);

  const dummyCampaigns = [
    {
      id: 1,
      name: "Summer Sale 2024",
      channel: "facebook",
      color: "#1877f2",
      date: "2024-01-15",
      time: "09:00",
      status: "scheduled"
    },
    {
      id: 2,
      name: "Product Launch",
      channel: "instagram",
      color: "#e4405f",
      date: "2024-01-20",
      time: "14:00",
      status: "scheduled"
    },
    {
      id: 3,
      name: "Brand Awareness",
      channel: "linkedin",
      color: "#0a66c2",
      date: "2024-01-25",
      time: "11:00",
      status: "draft"
    },
    {
      id: 4,
      name: "Holiday Special",
      channel: "google-ads",
      color: "#4285f4",
      date: "2024-02-10",
      time: "16:00",
      status: "scheduled"
    }
  ];

  useEffect(() => {
    setCampaigns(dummyCampaigns);
  }, []);

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    const days = [];
    for (let i = 0; i < firstDay; i++) {
      days.push(null);
    }
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(i);
    }
    return days;
  };

  const getCampaignsForDate = (day) => {
    const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return campaigns.filter(c => c.date === dateStr);
  };

  const getChannelIcon = (channel) => {
    const icons = {
      facebook: "📘",
      instagram: "📷",
      linkedin: "💼",
      twitter: "🐦",
      google: "🔍"
    };
    return icons[channel] || "📱";
  };

  const handleDateClick = (day) => {
    if (day) {
      setSelectedDate(day);
      setShowCreateModal(true);
    }
  };

  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];

  const days = getDaysInMonth(currentDate);

  return (
    <div className="data-section">
      <header className="page-header">
        <div>
          <h2>📅 Campaign Scheduler</h2>
          <p className="page-subtitle">Schedule posts and campaigns across multiple channels</p>
        </div>
        <button className="btn-primary" onClick={() => setShowCreateModal(true)}>
          ➕ Schedule Campaign
        </button>
      </header>

      <div className="scheduler-container">
        <div className="calendar-header">
          <button 
            className="nav-btn"
            onClick={() => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1))}
          >
            ◀
          </button>
          <h3>{monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}</h3>
          <button 
            className="nav-btn"
            onClick={() => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1))}
          >
            ▶
          </button>
        </div>

        <div className="calendar-grid">
          <div className="day-header">Sun</div>
          <div className="day-header">Mon</div>
          <div className="day-header">Tue</div>
          <div className="day-header">Wed</div>
          <div className="day-header">Thu</div>
          <div className="day-header">Fri</div>
          <div className="day-header">Sat</div>

          {days.map((day, index) => {
            const dayCampaigns = day ? getCampaignsForDate(day) : [];
            const hasCampaign = dayCampaigns.length > 0;
            
            return (
              <div
                key={index}
                className={`calendar-day ${day ? 'active' : 'empty'} ${hasCampaign ? 'has-campaign' : ''}`}
                onClick={() => handleDateClick(day)}
              >
                <span className="day-number">{day}</span>
                {hasCampaign && (
                  <div className="campaign-indicators">
                    {dayCampaigns.slice(0, 3).map((campaign, i) => (
                      <div
                        key={i}
                        className="campaign-dot"
                        style={{ backgroundColor: campaign.color }}
                        title={campaign.name}
                      >
                        {getChannelIcon(campaign.channel)}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="campaigns-legend">
          <h4>Channel Legend</h4>
          <div className="legend-items">
            <div className="legend-item">
              <span className="legend-icon">📘</span>
              <span>Facebook</span>
            </div>
            <div className="legend-item">
              <span className="legend-icon">📷</span>
              <span>Instagram</span>
            </div>
            <div className="legend-item">
              <span className="legend-icon">💼</span>
              <span>LinkedIn</span>
            </div>
            <div className="legend-item">
              <span className="legend-icon">🔍</span>
              <span>Google Ads</span>
            </div>
          </div>
        </div>
      </div>

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📅 Schedule Campaign</h3>
              <button className="modal-close" onClick={() => setShowCreateModal(false)}>✕</button>
            </div>
            <div className="modal-body">
              <div className="schedule-preview">
                <h4>📅 {selectedDate ? new Date(currentDate.getFullYear(), currentDate.getMonth(), selectedDate).toLocaleDateString() : 'Select Date'}</h4>
                <div className="existing-campaigns">
                  {selectedDate && getCampaignsForDate(selectedDate).length > 0 ? (
                    <div className="campaign-list">
                      {getCampaignsForDate(selectedDate).map((campaign) => (
                        <div key={campaign.id} className="existing-campaign">
                          <div className="campaign-header">
                            <span className="campaign-channel" style={{ backgroundColor: campaign.color }}>
                              {getChannelIcon(campaign.channel)}
                            </span>
                            <span className="campaign-name">{campaign.name}</span>
                            <span className={`campaign-status ${campaign.status}`}>
                              {campaign.status}
                            </span>
                          </div>
                          <div className="campaign-time">
                            🕐 {campaign.time}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="no-campaigns">
                      <p>No campaigns scheduled for this date</p>
                      <p>Click below to create a new campaign</p>
                    </div>
                  )}
                </div>
              </div>
              <form className="schedule-form">
                <div className="form-group">
                  <label>Campaign Name</label>
                  <input type="text" placeholder="Enter campaign name" className="form-input" />
                </div>
                <div className="form-group">
                  <label>Channel</label>
                  <select className="form-select">
                    <option value="">Select channel</option>
                    <option value="facebook">📘 Facebook</option>
                    <option value="instagram">📷 Instagram</option>
                    <option value="linkedin">💼 LinkedIn</option>
                    <option value="twitter">🐦 Twitter</option>
                    <option value="google">🔍 Google Ads</option>
                  </select>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Date</label>
                    <input 
                      type="date" 
                      className="form-input" 
                      defaultValue={selectedDate ? `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(selectedDate).padStart(2, '0')}` : ''}
                    />
                  </div>
                  <div className="form-group">
                    <label>Time</label>
                    <input type="time" className="form-input" defaultValue="09:00" />
                  </div>
                </div>
                <div className="form-group">
                  <label>Message</label>
                  <textarea placeholder="Enter campaign message" className="form-textarea" rows="4"></textarea>
                </div>
                <div className="form-actions">
                  <button type="button" className="btn-secondary" onClick={() => setShowCreateModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    ✨ Schedule Campaign
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
