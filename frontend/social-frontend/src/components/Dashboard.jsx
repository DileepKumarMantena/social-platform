import React from "react";

export default function Dashboard({ token }) {
  return (
    <div style={{ margin: "20px" }}>
      <h2>Dashboard</h2>
      <p>Logged in with token: <strong>{token}</strong></p>
    </div>
  );
}