import React, { useState } from "react";
import { createTenant, createUser, getTenants } from "../api";
import "./SuperAdminDashboard.css";

export default function SuperAdminDashboard({ auth }) {
  const [tenants, setTenants] = useState([]);
  const [users, setUsers] = useState([]);
  const [showCreateTenant, setShowCreateTenant] = useState(false);
  const [showCreateUser, setShowCreateUser] = useState(false);
  const [message, setMessage] = useState("");
  const [activeTab, setActiveTab] = useState("tenants");
  const [visiblePasswords, setVisiblePasswords] = useState({});

  const loadData = async () => {
    try {
      const tenantData = await getTenants(auth.token);
      setTenants(tenantData || []);
      // Load users from all tenants (in real app, this would be API call)
      setUsers([
        { username: "demo_lead", role: "lead", tenant_id: "tenant_123", tenant_name: "Demo Company" },
        { username: "demo_admin", role: "admin", tenant_id: "tenant_123", tenant_name: "Demo Company" },
        { username: "demo_user", role: "user", tenant_id: "tenant_123", tenant_name: "Demo Company" }
      ]);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  // Initialize with demo data only once
  React.useEffect(() => {
    setUsers([
      { username: "demo_lead", role: "lead", tenant_id: "tenant_123", tenant_name: "Demo Company", password: "Lead@123456" },
      { username: "demo_admin", role: "admin", tenant_id: "tenant_123", tenant_name: "Demo Company", password: "Admin@123456" },
      { username: "demo_user", role: "user", tenant_id: "tenant_123", tenant_name: "Demo Company", password: "User@123456" }
    ]);
    // Load initial tenants
    loadData();
  }, []);

  const togglePasswordVisibility = (username) => {
    setVisiblePasswords(prev => ({
      ...prev,
      [username]: !prev[username]
    }));
  };

  const handleDeleteTenant = async (tenantId) => {
    if (window.confirm(`Are you sure you want to delete tenant ${tenantId}? This will also delete all users in this tenant.`)) {
      try {
        // In real app, this would be API call
        setTenants(tenants.filter(t => t.id !== tenantId));
        setUsers(users.filter(u => u.tenant_id !== tenantId));
        setMessage(`Tenant ${tenantId} deleted successfully`);
      } catch (error) {
        setMessage(`Error deleting tenant: ${error.message}`);
      }
    }
  };

  const handleDeleteUser = async (username) => {
    if (window.confirm(`Are you sure you want to delete user ${username}?`)) {
      try {
        // In real app, this would be API call
        setUsers(users.filter(u => u.username !== username));
        setMessage(`User ${username} deleted successfully`);
      } catch (error) {
        setMessage(`Error deleting user: ${error.message}`);
      }
    }
  };

  const handleCreateTenant = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
      const result = await createTenant({
        name: formData.get("name")
      }, auth.token);
      setMessage(`Tenant created: ${result.tenant_id}`);
      setShowCreateTenant(false);
      
      // Add new tenant to local state with current date
      const newTenant = {
        id: result.tenant_id,
        name: formData.get("name"),
        status: "active",
        created_at: new Date().toISOString()
      };
      setTenants([...tenants, newTenant]);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
      const result = await createUser({
        username: formData.get("username"),
        password: formData.get("password"),
        role: formData.get("role"),
        tenant_id: formData.get("tenant_id"),
        access_days: formData.get("access_days") ? parseInt(formData.get("access_days")) : null
      }, auth.token);
      setMessage(`User created: ${result.user_id}`);
      setShowCreateUser(false);
      
      // Add new user to local state
      const tenantName = tenants.find(t => t.id === formData.get("tenant_id"))?.name || formData.get("tenant_id");
      let expiresAt = result.expires_at;
      
      // Calculate expiration date if access_days provided for any role
      const accessDays = formData.get("access_days") ? parseInt(formData.get("access_days")) : null;
      if (accessDays && formData.get("role") === "admin") {
        expiresAt = new Date(Date.now() + accessDays * 24 * 60 * 60 * 1000).toISOString();
      }
      
      const newUser = {
        username: formData.get("username"),
        role: formData.get("role"),
        tenant_id: formData.get("tenant_id"),
        tenant_name: tenantName,
        password: formData.get("password"),
        expires_at: expiresAt
      };
      setUsers([...users, newUser]);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div className="super-admin-dashboard">
      <div className="dashboard-header">
        <h1>Super Admin Dashboard</h1>
        <p>Welcome, {auth.user?.username}</p>
      </div>

      <div className="admin-actions">
        <div className="action-card">
          <h3>Create Tenant/Customer</h3>
          <button onClick={() => setShowCreateTenant(true)}>
            + New Tenant
          </button>
        </div>

        <div className="action-card">
          <h3>Create User</h3>
          <button onClick={() => setShowCreateUser(true)}>
            + New User
          </button>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={activeTab === "tenants" ? "active" : ""}
          onClick={() => setActiveTab("tenants")}
        >
          Tenants ({tenants.length})
        </button>
        <button 
          className={activeTab === "users" ? "active" : ""}
          onClick={() => setActiveTab("users")}
        >
          Users ({users.length})
        </button>
      </div>

      {activeTab === "tenants" && (
        <div className="data-table">
          <h3>Tenants/Customers</h3>
          <table>
            <thead>
              <tr>
                <th>Tenant ID</th>
                <th>Name</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {tenants.map(tenant => (
                <tr key={tenant.id}>
                  <td>{tenant.id}</td>
                  <td>{tenant.name}</td>
                  <td>{tenant.status}</td>
                  <td>{tenant.created_at ? new Date(tenant.created_at).toLocaleDateString() : 'N/A'}</td>
                  <td>
                    <button 
                      className="delete-btn" 
                      onClick={() => handleDeleteTenant(tenant.id)}
                      title="Delete Tenant"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === "users" && (
        <div className="data-table">
          <h3>All Users</h3>
          <table>
            <thead>
              <tr>
                <th>Username</th>
                <th>Role</th>
                <th>Tenant</th>
                <th>Password</th>
                <th>Expires</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.username}>
                  <td>{user.username}</td>
                  <td>{user.role}</td>
                  <td>{user.tenant_name}</td>
                  <td className="password-cell">
                    <span className="password-text">
                      {visiblePasswords[user.username] ? user.password : '••••••••'}
                    </span>
                    <button 
                      className="password-toggle-btn"
                      onClick={() => togglePasswordVisibility(user.username)}
                      title={visiblePasswords[user.username] ? "Hide password" : "Show password"}
                    >
                      {visiblePasswords[user.username] ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </td>
                  <td>
                    {user.expires_at 
                      ? new Date(user.expires_at).toLocaleDateString() 
                      : 'Never'}
                  </td>
                  <td>
                    <button 
                      className="delete-btn" 
                      onClick={() => handleDeleteUser(user.username)}
                      title="Delete User"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showCreateTenant && (
        <div className="modal">
          <div className="modal-content">
            <h2>Create New Tenant</h2>
            <form onSubmit={handleCreateTenant}>
              <input
                type="text"
                name="name"
                placeholder="Company Name"
                required
              />
              <div className="modal-actions">
                <button type="submit">Create</button>
                <button type="button" onClick={() => setShowCreateTenant(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showCreateUser && (
        <div className="modal">
          <div className="modal-content">
            <h2>Create New User</h2>
            <form onSubmit={handleCreateUser}>
              <input
                type="text"
                name="username"
                placeholder="Username"
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                required
              />
              <select name="role" required>
                <option value="">Select Role</option>
                <option value="lead">Lead</option>
                <option value="admin">Admin</option>
                <option value="user">User</option>
              </select>
              <input
                type="text"
                name="tenant_id"
                placeholder="Tenant ID"
                required
              />
              <input
                type="number"
                name="access_days"
                placeholder="Access Days (for Admin only)"
              />
              <div className="modal-actions">
                <button type="submit">Create</button>
                <button type="button" onClick={() => setShowCreateUser(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {message && (
        <div className="message">
          {message}
        </div>
      )}
    </div>
  );
}
