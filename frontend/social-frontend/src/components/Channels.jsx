import React, { useEffect, useState } from "react";
import { getChannels, toggleChannel } from "../AppUtils";

const CHANNEL_COLORS = {
  facebook: "#1877f2",
  instagram: "#e4405f",
  linkedin: "#0a66c2",
  twitter: "#1da1f2",
  youtube: "#ff0000",
  "google-ads": "#4285f4",
};

export default function Channels({ token, user }) {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [toggling, setToggling] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const canEdit = user?.role === "admin" || user?.role === "lead";

  const fetchChannels = async () => {
    try {
      const data = await getChannels(token);
      setChannels(Array.isArray(data) ? data : []);
    } catch {
      setChannels([]);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (channelId) => {
    const ch = channels.find((c) => c.id === channelId);
    const channelName = ch?.name || "Channel";
    const wasConnected = ch?.connected || ch?.active;

    setToggling(channelId);

    // Optimistic update – UI changes immediately
    setChannels((prev) =>
      prev.map((c) =>
        c.id === channelId ? { ...c, connected: !wasConnected, active: !wasConnected } : c
      )
    );

    try {
      await toggleChannel(channelId, token);
      setFeedback({
        type: "success",
        message: wasConnected ? `${channelName} disconnected` : `${channelName} connected`,
      });
      setTimeout(() => setFeedback(null), 2500);
    } catch (err) {
      // Revert on error
      setChannels((prev) =>
        prev.map((c) => (c.id === channelId ? { ...c, connected: wasConnected, active: wasConnected } : c))
      );
      const msg = err?.response?.data?.detail ?? err?.message ?? "Failed to update. Is the backend running?";
      setFeedback({ type: "error", message: msg });
      setTimeout(() => setFeedback(null), 3000);
    } finally {
      setToggling(null);
    }
  };

  useEffect(() => {
    fetchChannels();
  }, [token]);

  return (
    <div className="data-section">
      <header className="page-header">
        <h2>Channels</h2>
        <p className="page-subtitle">Connect your social media accounts and ad platforms</p>
      </header>
      {feedback && (
        <div className={`channel-feedback ${feedback.type}`}>
          {feedback.message}
        </div>
      )}
      {loading ? (
        <div className="loading-block">Loading channels...</div>
      ) : (
        <div className="channel-cards">
          {channels.map((ch) => {
            const slug = ch.slug || (ch.name || "").toLowerCase().replace(/\s+/g, "-") || "";
            const color = CHANNEL_COLORS[slug] || "#6366f1";
            const connected = ch.connected || ch.active;

            return (
              <div key={ch.id} className={`channel-card ${connected ? "connected" : ""}`}>
                <div className="channel-icon" style={{ backgroundColor: `${color}33`, color }}>
                  {ch.name?.charAt(0) || "?"}
                </div>
                <div className="channel-info">
                  <h4>{ch.name || "N/A"}</h4>
                  <span className={`channel-status ${connected ? "connected" : ""}`}>
                    {connected ? "Connected" : "Not connected"}
                  </span>
                </div>
                <button
                  type="button"
                  className={`channel-action-btn ${connected ? "disconnect" : ""}`}
                  onClick={() => handleToggle(ch.id)}
                  disabled={toggling === ch.id || !canEdit}
                  title={!canEdit ? "Read-only access" : ""}
                >
                  {toggling === ch.id ? "..." : connected ? "Disconnect" : "Connect"}
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
