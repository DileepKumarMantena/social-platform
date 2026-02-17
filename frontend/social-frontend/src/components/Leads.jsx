import React, { useEffect, useState } from "react";
import { getLeads, updateLeadStatus, getTenants } from "../AppUtils";

const STATUS_OPTIONS = ["new", "contacted", "qualified", "won", "lost"];

export default function Leads({ token, user }) {
  const [leads, setLeads] = useState([]);
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tenantFilter, setTenantFilter] = useState("");
  const [updating, setUpdating] = useState(null);

  const isSalesOrAdmin = ["sales", "admin"].includes(user?.role || "");

  const fetchLeads = async (tenantId = null) => {
    try {
      const data = await getLeads(token, tenantId || undefined);
      setLeads(Array.isArray(data) ? data : []);
    } catch {
      setLeads([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchTenants = async () => {
    try {
      const data = await getTenants(token);
      setTenants(Array.isArray(data) ? data : []);
    } catch {
      setTenants([]);
    }
  };

  useEffect(() => {
    fetchLeads(tenantFilter || null);
  }, [token, tenantFilter]);

  useEffect(() => {
    if (isSalesOrAdmin) fetchTenants();
  }, [token, isSalesOrAdmin]);

  const handleStatusChange = async (leadId, newStatus) => {
    setUpdating(leadId);
    try {
      await updateLeadStatus(leadId, newStatus, token);
      fetchLeads(tenantFilter || null);
    } catch {
      // Error
    } finally {
      setUpdating(null);
    }
  };

  return (
    <div className="data-section">
      <header className="page-header page-header-row">
        <div>
          <h2>Leads</h2>
          <p className="page-subtitle">Track and follow up on leads for {user?.tenant_name || "your company"}</p>
        </div>
        {isSalesOrAdmin && tenants.length > 0 && (
          <div className="filter-group">
            <label htmlFor="tenant-filter">Company:</label>
            <select
              id="tenant-filter"
              value={tenantFilter}
              onChange={(e) => setTenantFilter(e.target.value)}
              className="filter-select"
            >
              <option value="">My company</option>
              {tenants.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name || t.id}
                </option>
              ))}
            </select>
          </div>
        )}
      </header>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Company</th>
            <th>Status</th>
            <th>Follow up</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={6} className="loading-state">Loading...</td>
            </tr>
          ) : leads.length === 0 ? (
            <tr>
              <td colSpan={6} className="empty-state">No leads found</td>
            </tr>
          ) : (
            leads.map((l) => (
              <tr key={l.id}>
                <td>{l.id}</td>
                <td>{l.name || "N/A"}</td>
                <td>{l.email || "N/A"}</td>
                <td>{l.tenant_name || l.tenant_id || "—"}</td>
                <td>
                  <span className={`status-badge status-lead-${l.status || "new"}`}>
                    {l.status || "new"}
                  </span>
                </td>
                <td>
                  <select
                    className="status-select"
                    value={l.status || "new"}
                    onChange={(e) => handleStatusChange(l.id, e.target.value)}
                    disabled={updating === l.id}
                  >
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
