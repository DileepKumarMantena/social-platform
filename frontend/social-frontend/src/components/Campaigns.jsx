import React, { useEffect, useState } from "react";
import { getCampaigns } from "../App";

export default function Campaigns({ token }) {
  const [campaigns, setCampaigns] = useState([]);

  const fetchCampaigns = async () => {
    const data = await getCampaigns(token);
    setCampaigns(data);
  };

  useEffect(() => {
    fetchCampaigns();
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <h3>Campaigns</h3>
      <ul>
        {campaigns.map((c) => (
          <li key={c.id}>
            {c.name} | Platform: {c.channel_name} | Budget: {c.budget}
          </li>
        ))}
      </ul>
    </div>
  );
}