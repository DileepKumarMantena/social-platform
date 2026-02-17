// App.jsx
import React, { useState } from "react";
import Login from "./components/Login";      // correct import
import Channels from "./components/Channels";
import Campaigns from "./components/Campaigns";
import Leads from "./components/Leads";

function App() {
  const [token, setToken] = useState(null);

  if (!token) return <Login setToken={setToken} />;

  return (
    <div>
      <h1>Dashboard</h1>
      <Channels token={token} />
      <Campaigns token={token} />
      <Leads token={token} />
    </div>
  );
}

export default App;