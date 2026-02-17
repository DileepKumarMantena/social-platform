import React, { useEffect, useState } from "react";
import { getLeads } from "../App";

export default function Leads({ token }) {
  const [leads, setLeads] = useState([]);

  const fetchLeads = async () => {
    const data = await getLeads(token);
    setLeads(data);
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <h3>Leads</h3>
      <ul>
        {leads.map((l) => (
          <li key={l.id}>
            {l.name} | Email: {l.email || "N/A"}
          </li>
        ))}
      </ul>
    </div>
  );
}