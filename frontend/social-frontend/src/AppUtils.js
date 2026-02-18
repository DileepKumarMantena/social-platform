import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

// AUTH
export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/login`, { username, password });
  return response.data;
};

export const register = async (username, password, tenantName, role = "user") => {
  const response = await axios.post(`${API_URL}/register`, {
    username,
    password,
    tenant_name: tenantName,
    role,
  });
  return response.data;
};

export const changePassword = async (currentPassword, newPassword, token) => {
  const response = await axios.post(
    `${API_URL}/change-password`,
    { current_password: currentPassword, new_password: newPassword },
    { headers: { Authorization: `Bearer ${token}` } }
  );
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
export const getLeads = async (token, tenantId = null) => {
  const params = tenantId ? { tenant_id: tenantId } : {};
  const response = await axios.get(`${API_URL}/leads`, {
    headers: { Authorization: `Bearer ${token}` },
    params,
  });
  return response.data;
};

export const createLead = async (lead, token) => {
  const response = await axios.post(`${API_URL}/leads`, lead, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const updateLeadStatus = async (leadId, status, token) => {
  const response = await axios.post(
    `${API_URL}/leads/${leadId}/status`,
    { status },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

// TENANTS
export const getTenants = async (token) => {
  const response = await axios.get(`${API_URL}/tenants`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// DASHBOARD STATS
export const getCampaignStats = async (token) => {
  const response = await axios.get(`${API_URL}/campaigns/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};