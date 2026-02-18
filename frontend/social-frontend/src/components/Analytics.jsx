import React, { useEffect, useState } from "react";
import "./Analytics.css";

export default function Analytics({ token, user }) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="data-section">
        <div className="loading-state">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="data-section">
      <header className="page-header">
        <div>
          <h2>📈 Analytics Dashboard</h2>
          <p className="page-subtitle">Performance insights and recommendations</p>
        </div>
      </header>

      <div className="analytics-content">
        <div className="analytics-grid">
          <div className="analytics-card">
            <div className="card-icon">🎯</div>
            <h3>Top Performing Channels</h3>
            <div className="channel-stats">
              <div className="channel-stat">
                <span className="channel-name">📘 Facebook</span>
                <span className="channel-value">45%</span>
              </div>
              <div className="channel-stat">
                <span className="channel-name">📷 Instagram</span>
                <span className="channel-value">30%</span>
              </div>
              <div className="channel-stat">
                <span className="channel-name">💼 LinkedIn</span>
                <span className="channel-value">25%</span>
              </div>
            </div>
            <div className="mini-chart">
              <div className="chart-bar" style={{ height: "60%" }}></div>
              <div className="chart-bar" style={{ height: "80%" }}></div>
              <div className="chart-bar" style={{ height: "45%" }}></div>
              <div className="chart-bar" style={{ height: "90%" }}></div>
              <div className="chart-bar" style={{ height: "70%" }}></div>
            </div>
          </div>

          <div className="analytics-card">
            <div className="card-icon">⏰</div>
            <h3>Optimal Posting Times</h3>
            <div className="time-slots">
              <div className="time-slot">
                <span className="time">9:00 AM</span>
                <span className="engagement">High</span>
              </div>
              <div className="time-slot">
                <span className="time">12:00 PM</span>
                <span className="engagement">Medium</span>
              </div>
              <div className="time-slot">
                <span className="time">6:00 PM</span>
                <span className="engagement">High</span>
              </div>
              <div className="time-slot">
                <span className="time">8:00 PM</span>
                <span className="engagement">Medium</span>
              </div>
            </div>
          </div>

          <div className="analytics-card">
            <div className="card-icon">💡</div>
            <h3>Smart Recommendations</h3>
            <div className="recommendations">
              <div className="recommendation">
                <span className="rec-icon">🎯</span>
                <span className="rec-text">Focus on Instagram for higher engagement</span>
              </div>
              <div className="recommendation">
                <span className="rec-icon">📈</span>
                <span className="rec-text">Post at 6 PM for optimal reach</span>
              </div>
              <div className="recommendation">
                <span className="rec-icon">💰</span>
                <span className="rec-text">Increase budget by 20% for Facebook</span>
              </div>
            </div>
          </div>

          <div className="analytics-card">
            <div className="card-icon">📱</div>
            <h3>Audience Demographics</h3>
            <div className="demographics">
              <div className="demo-item">
                <span className="demo-label">18-24 years</span>
                <span className="demo-value">35%</span>
              </div>
              <div className="demo-item">
                <span className="demo-label">25-34 years</span>
                <span className="demo-value">40%</span>
              </div>
              <div className="demo-item">
                <span className="demo-label">35-44 years</span>
                <span className="demo-value">25%</span>
              </div>
            </div>
          </div>

          <div className="analytics-card">
            <div className="card-icon">🔥</div>
            <h3>Trending Content</h3>
            <div className="trending-content">
              <div className="trend-item">
                <span className="trend-emoji">📸</span>
                <span className="trend-text">Photo posts get 2x more engagement</span>
              </div>
              <div className="trend-item">
                <span className="trend-emoji">🎥</span>
                <span className="trend-text">Video content trending upward</span>
              </div>
              <div className="trend-item">
                <span className="trend-emoji">📝</span>
                <span className="trend-text">Story format performing well</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
