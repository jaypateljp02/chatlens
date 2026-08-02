import axios from 'axios';

// Live Render Backend URL (Change to http://10.0.2.2:8000 for local Android emulator testing)
export const API_URL = 'https://chatlens-backend.onrender.com/api'; // Replace with actual Render URL

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadChat = async (fileData) => {
  const formData = new FormData();
  formData.append('file', {
    uri: fileData.uri,
    name: fileData.name || 'chat.txt',
    type: fileData.type || 'text/plain',
  });

  const response = await axios.post(`${API_URL}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const getActionItems = async (chatId = 'all') => {
  const response = await apiClient.get(`/extracted/${chatId}?type=task`);
  return response.data;
};

export const askQuestion = async (chatId, question) => {
  const response = await apiClient.post(`/qa/${chatId}`, { question });
  return response.data;
};
