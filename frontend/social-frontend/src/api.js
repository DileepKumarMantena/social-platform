import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

// If you need auth token later, you can pass it in headers
export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/login`, { username, password });
  return response.data;
};

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