import axios from 'axios';

const API_BASE_URL = 'https://foggy-object-detection-fullstack-ai-app-1.onrender.com';

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getResults = async (jobId) => {
  const response = await axios.get(`${API_BASE_URL}/results/${jobId}`);
  return response.data;
};

export const getFileUrl = (path) => {
  if (!path) return null;
  return `${API_BASE_URL}${path}`;
};
