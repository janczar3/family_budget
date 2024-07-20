import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const registerUser = async (username, password, passwordConfirm) => {
  try {
    const response = await apiClient.post('/family-budget/user-register/', {
      username,
      password,
      password_confirm: passwordConfirm,
    });
    return response;
  } catch (error) {
    throw error;
  }
};
