import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

// LOGIN
export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/login`, { username, password });
  return response.data;
};

// CHANNELS
export const getChannels = async (token) => {
  const response = await axios.get(`${API_URL}/channels`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const toggleChannel = async (channel_id, token) => {
  const response = await axios.post(
    `${API_URL}/channels/toggle`,
    { channel_id },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

// CAMPAIGNS
export const getCampaigns = async (token) => {
  const response = await axios.get(`${API_URL}/campaigns`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const createCampaign = async (campaign, token) => {
  const response = await axios.post(`${API_URL}/campaigns`, campaign, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// LEADS
export const getLeads = async (token) => {
  const response = await axios.get(`${API_URL}/leads`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};