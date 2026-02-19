import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1";

// Generic API request function
export const apiRequest = async (endpoint, method = "GET", data = null, token = null) => {
  const config = {
    method,
    url: `${API_URL}${endpoint}`,
  };
  
  if (data) {
    config.data = data;
  }
  
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  
  const response = await axios(config);
  return response.data;
};

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

export const getCampaigns = async (token) => {
  const response = await axios.get(`${API_URL}/campaigns`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const getLeads = async (token) => {
  const response = await axios.get(`${API_URL}/leads`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const getTenants = async (token) => {
  const response = await axios.get(`${API_URL}/tenants`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const createTenant = async (tenantData, token) => {
  const response = await axios.post(`${API_URL}/create-tenant`, tenantData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const createUser = async (userData, token) => {
  const response = await axios.post(`${API_URL}/create-user`, userData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};