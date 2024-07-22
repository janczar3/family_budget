import apiClient from "./base";

const ACCESS_TOKEN_KEY = 'access';
const REFRESH_TOKEN_KEY = 'refresh';

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
  localStorage.setItem(ACCESS_TOKEN_KEY, response.data[ACCESS_TOKEN_KEY]);
  localStorage.setItem(REFRESH_TOKEN_KEY, response.data[REFRESH_TOKEN_KEY]);
  return response.data;
};

export const logoutUser = async () => {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
  if (!refreshToken) throw new Error('No refresh token available');
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  const response = await apiClient.post('/family-budget/users/logout/', {
    refresh: refreshToken,
  });
  return response.data;
};

export const checkIfLoggedIn = async () => {
  const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY);
  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
  if (!accessToken || !refreshToken) {
    return false;
  }

  try {
    const response = await apiClient.get('/family-budget/user/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data.code === 'token_not_valid') {
      try {
        const refreshResponse = await apiClient.post('/family-budget/token/refresh/', {
          refresh: refreshToken,
        });
        localStorage.setItem(ACCESS_TOKEN_KEY, refreshResponse.data[ACCESS_TOKEN_KEY]);
        return checkIfLoggedIn();
      } catch (refreshError) {
        console.error('Error refreshing token', refreshError);
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        return false;
      }
    }
    console.error('Error checking if logged in', error);
    return false;
  }
};
