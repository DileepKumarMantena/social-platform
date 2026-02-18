import React, { useState } from "react";
import { register } from "../AppUtils";
import { Link } from "react-router-dom";

export default function Register({ setAuth }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [tenantName, setTenantName] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const data = await register(username, password, tenantName);
      setAuth({
        token: data.access_token,
        user: data.user,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <h2>Register</h2>
        <p className="login-subtitle">Create your account</p>
        <form onSubmit={handleSubmit} className="login-form">
          <table>
            <tbody>
              <tr>
                <td>
                  <label htmlFor="username">Username</label>
                </td>
                <td>
                  <input
                    id="username"
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <label htmlFor="password">Password</label>
                </td>
                <td>
                  <input
                    id="password"
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <label htmlFor="tenantName">Company Name</label>
                </td>
                <td>
                  <input
                    id="tenantName"
                    type="text"
                    placeholder="Company Name"
                    value={tenantName}
                    onChange={(e) => setTenantName(e.target.value)}
                    required
                  />
                </td>
              </tr>
              <tr>
                <td />
                <td className="btn-cell">
                  <button type="submit">Register</button>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
        {error && <p className="login-error">{error}</p>}
        <p style={{ marginTop: "1rem", textAlign: "center" }}>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}
