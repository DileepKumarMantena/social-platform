import React, { useEffect, useState } from "react";
import { getChannels, toggleChannel } from "../AppUtils";

export default function Channels({ token }) {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);

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
    try {
      await toggleChannel(channelId, token);
      fetchChannels();
    } catch {
      // Error handled - could add toast/notification
    }
  };

  useEffect(() => {
    fetchChannels();
  }, []);

  return (
    <div className="data-section">
      <header className="page-header">
        <h2>Channels</h2>
        <p className="page-subtitle">Manage your marketing channels</p>
      </header>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Active</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={4} className="loading-state">Loading...</td>
            </tr>
          ) : channels.length === 0 ? (
            <tr>
              <td colSpan={4} className="empty-state">No channels found</td>
            </tr>
          ) : (
            channels.map((ch) => (
              <tr key={ch.id}>
                <td>{ch.id}</td>
                <td>{ch.name || "N/A"}</td>
                <td>{ch.active ? "Yes" : "No"}</td>
                <td>
                  <button type="button" onClick={() => handleToggle(ch.id)}>
                    {ch.active ? "Deactivate" : "Activate"}
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
