import React, { useEffect, useState } from "react";
import { getCampaigns, createCampaign, getChannels } from "../AppUtils";

export default function Campaigns({ token }) {
  const [campaigns, setCampaigns] = useState([]);
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [channelId, setChannelId] = useState("");
  const [budget, setBudget] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const fetchCampaigns = async () => {
    try {
      const data = await getCampaigns(token);
      setCampaigns(Array.isArray(data) ? data : []);
    } catch {
      setCampaigns([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchChannels = async () => {
    try {
      const data = await getChannels(token);
      setChannels(Array.isArray(data) ? data : []);
    } catch {
      setChannels([]);
    }
  };

  useEffect(() => {
    fetchCampaigns();
    fetchChannels();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    if (!channelId) {
      setError("Please select a channel");
      return;
    }
    setSubmitting(true);
    try {
      await createCampaign(
        {
          name: name.trim(),
          channel_id: parseInt(channelId, 10),
          budget: parseFloat(budget) || 0,
        },
        token
      );
      setName("");
      setChannelId("");
      setBudget("");
      setShowForm(false);
      setLoading(true);
      await fetchCampaigns();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create campaign");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="data-section">
      <header className="page-header page-header-row">
        <div>
          <h2>Campaigns</h2>
          <p className="page-subtitle">View and manage your campaigns</p>
        </div>
        <button
          type="button"
          className="btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Cancel" : "Add Campaign"}
        </button>
      </header>
      {showForm && (
        <form onSubmit={handleCreate} className="campaign-form">
          <table>
            <tbody>
              <tr>
                <td><label htmlFor="camp-name">Name</label></td>
                <td>
                  <input
                    id="camp-name"
                    type="text"
                    placeholder="Campaign name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </td>
              </tr>
              <tr>
                <td><label htmlFor="camp-channel">Channel</label></td>
                <td>
                  <select
                    id="camp-channel"
                    value={channelId}
                    onChange={(e) => setChannelId(e.target.value)}
                  >
                    <option value="">Select channel</option>
                    {channels.map((ch) => (
                      <option key={ch.id} value={ch.id}>
                        {ch.name}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
              <tr>
                <td><label htmlFor="camp-budget">Budget</label></td>
                <td>
                  <input
                    id="camp-budget"
                    type="number"
                    step="0.01"
                    min="0"
                    placeholder="0"
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                  />
                </td>
              </tr>
              <tr>
                <td />
                <td className="btn-cell">
                  <button type="submit" disabled={submitting}>
                    {submitting ? "Creating..." : "Create Campaign"}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          {error && <p className="form-error">{error}</p>}
        </form>
      )}
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Platform</th>
            <th>Budget</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={4} className="loading-state">Loading...</td>
            </tr>
          ) : campaigns.length === 0 ? (
            <tr>
              <td colSpan={4} className="empty-state">No campaigns found</td>
            </tr>
          ) : (
            campaigns.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.name || "N/A"}</td>
                <td>{c.channel_name || "N/A"}</td>
                <td>{c.budget ?? "N/A"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}