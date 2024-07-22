import apiClient from "./base";

const BASE_BUDGET_URL = '/family-budget/budgets';

export const listBudgets = async () => {
  return await apiClient.get(`${BASE_BUDGET_URL}/`);
};
