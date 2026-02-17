import React, { useState, useEffect } from "react";
import { changePassword } from "../AppUtils";

const PREF_KEYS = {
  notifyLeads: "socialmark-pref-notify-leads",
  weeklyDigest: "socialmark-pref-weekly-digest",
};

export default function Settings({ token, user, theme = "dark", onThemeChange = () => {} }) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState({ type: "", text: "" });
  const [submitting, setSubmitting] = useState(false);

  const [notifyLeads, setNotifyLeads] = useState(() => localStorage.getItem(PREF_KEYS.notifyLeads) === "true");
  const [weeklyDigest, setWeeklyDigest] = useState(() => localStorage.getItem(PREF_KEYS.weeklyDigest) === "true");

  useEffect(() => {
    localStorage.setItem(PREF_KEYS.notifyLeads, notifyLeads);
  }, [notifyLeads]);
  useEffect(() => {
    localStorage.setItem(PREF_KEYS.weeklyDigest, weeklyDigest);
  }, [weeklyDigest]);

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: "", text: "" });
    if (!currentPassword.trim()) {
      setMessage({ type: "error", text: "Enter your current password" });
      return;
    }
    if (!newPassword.trim()) {
      setMessage({ type: "error", text: "Enter a new password" });
      return;
    }
    if (newPassword.length < 4) {
      setMessage({ type: "error", text: "New password must be at least 4 characters" });
      return;
    }
    if (newPassword !== confirmPassword) {
      setMessage({ type: "error", text: "New passwords do not match" });
      return;
    }
    setSubmitting(true);
    try {
      await changePassword(currentPassword, newPassword, token);
      setMessage({ type: "success", text: "Password updated successfully." });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setMessage({
        type: "error",
        text: err.response?.data?.detail || "Failed to change password",
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="data-section">
      <header className="page-header">
        <h2>Settings</h2>
        <p className="page-subtitle">Manage your account and preferences</p>
      </header>

      <div className="settings-grid">
        {/* Profile */}
        <section className="settings-card">
          <h3>Profile</h3>
          <dl className="profile-list">
            <div className="profile-row">
              <dt>Username</dt>
              <dd>{user?.username || "—"}</dd>
            </div>
            <div className="profile-row">
              <dt>Company</dt>
              <dd>{user?.tenant_name || "—"}</dd>
            </div>
            <div className="profile-row">
              <dt>Role</dt>
              <dd style={{ textTransform: "capitalize" }}>{user?.role || "—"}</dd>
            </div>
          </dl>
        </section>

        {/* Change password */}
        <section className="settings-card">
          <h3>Change password</h3>
          <form onSubmit={handlePasswordSubmit} className="campaign-form" style={{ marginBottom: 0 }}>
            {message.text && (
              <div className={`settings-message ${message.type}`} style={{ marginBottom: "1rem", padding: "0.75rem", borderRadius: "6px", backgroundColor: message.type === "success" ? "#e8f5e9" : "#ffebee", color: message.type === "success" ? "#2e7d32" : "#c62828" }}>
                {message.text}
              </div>
            )}
            <table>
              <tbody>
                <tr>
                  <td><label htmlFor="current-password">Current password</label></td>
                  <td>
                    <input id="current-password" type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} placeholder="Enter current password" autoComplete="current-password" />
                  </td>
                </tr>
                <tr>
                  <td><label htmlFor="new-password">New password</label></td>
                  <td>
                    <input id="new-password" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} placeholder="At least 4 characters" autoComplete="new-password" />
                  </td>
                </tr>
                <tr>
                  <td><label htmlFor="confirm-password">Confirm new password</label></td>
                  <td>
                    <input id="confirm-password" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="Confirm new password" autoComplete="new-password" />
                  </td>
                </tr>
                <tr>
                  <td />
                  <td>
                    <button type="submit" className="btn-primary" disabled={submitting}>
                      {submitting ? "Updating..." : "Change password"}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </form>
        </section>

        {/* Preferences */}
        <section className="settings-card">
          <h3>Preferences</h3>
          <div className="settings-toggle-row">
            <div>
              <div className="settings-toggle-label">Theme</div>
              <div className="settings-toggle-desc">Choose light or dark appearance</div>
            </div>
            <div className="settings-theme-options">
              <button type="button" className={theme === "dark" ? "active" : ""} onClick={() => onThemeChange("dark")}>Dark</button>
              <button type="button" className={theme === "light" ? "active" : ""} onClick={() => onThemeChange("light")}>Light</button>
            </div>
          </div>
          <div className="settings-toggle-row">
            <div>
              <div className="settings-toggle-label">New lead notifications</div>
              <div className="settings-toggle-desc">Get notified when a new lead is added</div>
            </div>
            <button type="button" className={`toggle-switch ${notifyLeads ? "on" : ""}`} onClick={() => setNotifyLeads((v) => !v)} aria-label="Toggle new lead notifications" />
          </div>
          <div className="settings-toggle-row">
            <div>
              <div className="settings-toggle-label">Weekly digest</div>
              <div className="settings-toggle-desc">Receive a weekly summary of campaigns and leads</div>
            </div>
            <button type="button" className={`toggle-switch ${weeklyDigest ? "on" : ""}`} onClick={() => setWeeklyDigest((v) => !v)} aria-label="Toggle weekly digest" />
          </div>
        </section>

        {/* About */}
        <section className="settings-card">
          <h3>About</h3>
          <p className="about-meta">SocialMark — Social marketing platform. Version 1.0</p>
        </section>
      </div>
    </div>
  );
}
