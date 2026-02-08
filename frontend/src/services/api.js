import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Transactions
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return api.post('/api/transactions/upload-csv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getTransactions = async (params = {}) => {
  return api.get('/api/transactions', { params });
};

export const getTransaction = async (transactionId) => {
  return api.get(`/api/transactions/${transactionId}`);
};

// Analysis
export const analyzeTransactions = async (data) => {
  return api.post('/api/analysis/analyze', data);
};

export const trainModel = async (minTransactions = 100) => {
  return api.post('/api/analysis/train-model', null, {
    params: { min_transactions: minTransactions }
  });
};

export const getModelInfo = async () => {
  return api.get('/api/analysis/model-info');
};

// Alerts
export const getAlerts = async (params = {}) => {
  return api.get('/api/alerts', { params });
};

export const getAlert = async (alertId) => {
  return api.get(`/api/alerts/${alertId}`);
};

export const updateAlert = async (alertId, data) => {
  return api.put(`/api/alerts/${alertId}`, data);
};

export const deleteAlert = async (alertId) => {
  return api.delete(`/api/alerts/${alertId}`);
};

// Statistics
export const getStats = async () => {
  return api.get('/api/stats');
};

export const getDailyStats = async (days = 30) => {
  return api.get('/api/stats/daily', { params: { days } });
};

export const getStatsByCategory = async () => {
  return api.get('/api/stats/by-category');
};

export const getStatsBySeverity = async () => {
  return api.get('/api/stats/by-severity');
};

export default api;
