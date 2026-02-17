import React, { useEffect, useState } from "react";
import { getLeads } from "../AppUtils";

export default function Leads({ token }) {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLeads = async () => {
    try {
      const data = await getLeads(token);
      setLeads(Array.isArray(data) ? data : []);
    } catch {
      setLeads([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  return (
    <div className="data-section">
      <header className="page-header">
        <h2>Leads</h2>
        <p className="page-subtitle">Browse and track your leads</p>
      </header>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={3} className="loading-state">Loading...</td>
            </tr>
          ) : leads.length === 0 ? (
            <tr>
              <td colSpan={3} className="empty-state">No leads found</td>
            </tr>
          ) : (
            leads.map((l) => (
              <tr key={l.id}>
                <td>{l.id}</td>
                <td>{l.name || "N/A"}</td>
                <td>{l.email || "N/A"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}