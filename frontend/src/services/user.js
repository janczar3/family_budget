import apiClient from "./base";


export const registerUser = async (username, password, passwordConfirm) => {
  return await apiClient.post('/family-budget/users/register/', {
    username,
    password,
    password_confirm: passwordConfirm,
  });
};

export const loginUser = async (username, password) => {
  const response = await apiClient.post('/family-budget/users/login/', {
    username,
    password,
  });
  localStorage.setItem('access_token', response.data.access);
  localStorage.setItem('refresh_token', response.data.refresh);
  return response.data;
};

export const logoutUser = async () => {
  localStorage.getItem('refresh_token');
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) throw new Error('No refresh token available');
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  const response = await apiClient.post('/family-budget/users/logout/', {
    refresh_token: refreshToken,
  });
  return response.data;
};
