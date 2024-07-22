import apiClient from "./base";

const BASE_BUDGET_URL = '/family-budget/budgets';

export const listBudgets = async (page = null) => {
  const url = page? page : `${BASE_BUDGET_URL}/`;
  return await apiClient.get(url);
};

export const createBudget = async (data) => {
  return await apiClient.post(`${BASE_BUDGET_URL}/`, data);
};

export const deleteBudget = async (id) => {
  return await apiClient.delete(`${BASE_BUDGET_URL}/${id}/`,);
};