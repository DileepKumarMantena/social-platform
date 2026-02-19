import React, { useEffect, useState } from "react";
import { getLeads, updateLeadStatus, getTenants, createLead } from "../AppUtils";

const STATUS_OPTIONS = ["new", "contacted", "qualified", "won", "lost"];

export default function Leads({ token, user }) {
  const [leads, setLeads] = useState([]);
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tenantFilter, setTenantFilter] = useState(""); // set to user?.tenant_id when user loads for admin/sales
  const [updating, setUpdating] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formName, setFormName] = useState("");
  const [formEmail, setFormEmail] = useState("");
  const [formTenantId, setFormTenantId] = useState("");
  const [formStatus, setFormStatus] = useState("new");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const isSalesOrAdmin = ["sales", "admin"].includes(user?.role || "");
  const canEdit = user?.role === "lead";

  const fetchLeads = async (tenantId = null) => {
    try {
      const data = await getLeads(token, tenantId && tenantId !== "" ? tenantId : undefined);
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

  // Default to current user's company so leads are always for one company
  useEffect(() => {
    if (user?.tenant_id && isSalesOrAdmin && tenantFilter === "") {
      setTenantFilter(user.tenant_id);
    }
  }, [user?.tenant_id, isSalesOrAdmin]);

  useEffect(() => {
    if (!isSalesOrAdmin) {
      fetchLeads(null);
      return;
    }
    fetchLeads(tenantFilter || null);
  }, [token, tenantFilter, isSalesOrAdmin]);

  useEffect(() => {
    if (isSalesOrAdmin) fetchTenants();
  }, [token, isSalesOrAdmin]);

  const handleStatusChange = async (leadId, newStatus) => {
    setUpdating(leadId);
    try {
      await updateLeadStatus(leadId, newStatus, token);
      fetchLeads(tenantFilter || null);
    } catch {
      console.error("Failed to update lead status");
    } finally {
      setUpdating(null);
    }
  };

  const handleDeleteLead = async (leadId) => {
    if (window.confirm("Are you sure you want to delete this lead?")) {
      try {
        // In real app, this would be API call to delete lead
        setLeads(leads.filter(l => l.id !== leadId));
      } catch {
        console.error("Failed to delete lead");
      }
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    if (!formName.trim()) {
      setError("Name is required");
      return;
    }
    if (!formEmail.trim()) {
      setError("Email is required");
      return;
    }
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formEmail.trim())) {
      setError("Please enter a valid email address");
      return;
    }
    setSubmitting(true);
    try {
      await createLead(
        {
          name: formName.trim(),
          email: formEmail.trim(),
          tenant_id: formTenantId || undefined,
          status: formStatus,
        },
        token
      );
      setFormName("");
      setFormEmail("");
      setFormTenantId("");
      setFormStatus("new");
      setShowForm(false);
      setLoading(true);
      await fetchLeads(tenantFilter || null);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create lead");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="data-section">
      <header className="page-header page-header-row">
        <div>
          <h2>Leads</h2>
          <p className="page-subtitle">Track and follow up on leads for {user?.tenant_name || "your company"}</p>
        </div>
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          {isSalesOrAdmin && tenants.length > 0 && (
            <div className="filter-group">
              <label htmlFor="tenant-filter">Company:</label>
              <select
                id="tenant-filter"
                value={tenantFilter || user?.tenant_id || ""}
                onChange={(e) => setTenantFilter(e.target.value)}
                className="filter-select"
              >
                {tenants.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name || t.id}
                  </option>
                ))}
              </select>
            </div>
          )}
          {canEdit && (
            <button type="button" className="btn-primary" onClick={() => setShowForm(!showForm)}>
              {showForm ? "Cancel" : "Add Lead"}
            </button>
          )}
        </div>
      </header>
      {showForm && (
        <form onSubmit={handleCreate} className="campaign-form" style={{ marginBottom: "1.5rem" }}>
          {error && <div className="leads-error-message" style={{ marginBottom: "1rem", color: "#d32f2f" }}>{error}</div>}
          <table>
            <tbody>
              <tr>
                <td><label htmlFor="lead-name">Name *</label></td>
                <td>
                  <input
                    id="lead-name"
                    type="text"
                    value={formName}
                    onChange={(e) => setFormName(e.target.value)}
                    placeholder="Enter lead name"
                    required
                  />
                </td>
              </tr>
              <tr>
                <td><label htmlFor="lead-email">Email *</label></td>
                <td>
                  <input
                    id="lead-email"
                    type="email"
                    value={formEmail}
                    onChange={(e) => setFormEmail(e.target.value)}
                    placeholder="Enter email address"
                    required
                  />
                </td>
              </tr>
              {isSalesOrAdmin && tenants.length > 0 && (
                <tr>
                  <td><label htmlFor="lead-tenant">Company</label></td>
                  <td>
                    <select
                      id="lead-tenant"
                      value={formTenantId}
                      onChange={(e) => setFormTenantId(e.target.value)}
                    >
                      <option value="">Use my company</option>
                      {tenants.map((t) => (
                        <option key={t.id} value={t.id}>
                          {t.name || t.id}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              )}
              <tr>
                <td><label htmlFor="lead-status">Status</label></td>
                <td>
                  <select
                    id="lead-status"
                    value={formStatus}
                    onChange={(e) => setFormStatus(e.target.value)}
                  >
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
              <tr>
                <td></td>
                <td>
                  <button type="submit" className="btn-primary" disabled={submitting}>
                    {submitting ? "Creating..." : "Create Lead"}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
      )}
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Date</th>
            <th>Follow up</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={8} className="loading-state">Loading...</td>
            </tr>
          ) : leads.length === 0 ? (
            <tr>
              <td colSpan={8} className="empty-state">No leads found</td>
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
                <td>{l.created_at ? new Date(l.created_at).toLocaleDateString(undefined, { dateStyle: "short" }) : "—"}</td>
                <td>
                  <select
                    className="status-select"
                    value={l.status || "new"}
                    onChange={(e) => handleStatusChange(l.id, e.target.value)}
                    disabled={updating === l.id}
                  >
                    {STATUS_OPTIONS.map((status) => (
                      <option key={status} value={status}>
                        {status.charAt(0).toUpperCase() + status.slice(1)}
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <button 
                    className="delete-btn" 
                    onClick={() => handleDeleteLead(l.id)}
                    title="Delete Lead"
                    disabled={updating === l.id}
                    style={{
                      background: '#dc3545',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '6px 10px',
                      cursor: 'pointer',
                      fontSize: '0.9rem',
                      transition: 'background 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.background = '#c82333';
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.background = '#dc3545';
                    }}
                  >
                    🗑️
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
