import React, { useState } from "react";
import { login } from "../AppUtils";

export default function Login({ setAuth }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const data = await login(username, password);
      setAuth({
        token: data.access_token,
        user: data.user || { username: data.access_token, tenant_name: "Demo", role: "user" },
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <h2>Login</h2>
        <p className="login-subtitle">Sign in to access your dashboard</p>
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
                  />
                </td>
              </tr>
              <tr>
                <td />
                <td className="btn-cell">
                  <button type="submit">Login</button>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}