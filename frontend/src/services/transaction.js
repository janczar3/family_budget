import apiClient from "./base";

const BASE_INCOME_URL = '/family-budget/incomes';
const BASE_EXPENSE_URL = '/family-budget/expenses';


export const createIncome = async (data) => {
  return await apiClient.post(`${BASE_INCOME_URL}/`, data);
};

export const deleteIncome = async (id) => {
  return await apiClient.delete(`${BASE_INCOME_URL}/${id}/`,);
};


export const createExpense = async (data) => {
  return await apiClient.post(`${BASE_EXPENSE_URL}/`, data);
};

export const deleteExpense = async (id) => {
  return await apiClient.delete(`${BASE_EXPENSE_URL}/${id}/`,);
};