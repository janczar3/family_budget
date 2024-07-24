import React, {useState} from 'react';
import TransactionList from "../transaction/TransactionList";


function BudgetListItem({budget, handleDeleteBudget, fetchBudgets}) {
  const [budgetsShowDetails, setBudgetsShowDetails] = useState([]);

  const toggleBudgetDetails = (id) => {
    if (budgetsShowDetails.includes(id)) {
      setBudgetsShowDetails(budgetsShowDetails.filter(budgetId => budgetId !== id));
    } else {
      setBudgetsShowDetails([...budgetsShowDetails, id]);
    }
  };
  return (
    <>
    <a href="#" onClick={() => toggleBudgetDetails(budget.id)}>{budget.name} [{budget.total}] </a>
    <button onClick={() => handleDeleteBudget(budget.id)}>delete</button>
    {budgetsShowDetails.includes(budget.id) && (
      <>
        <div>
          {budget.user_names.length ? (
            <>
              <span>Budget members:</span>
              <ul>
                {budget.user_names.map((username) => (
                  <li key={username}>{username}</li>
                ))}
              </ul>
            </>
          ): <span>no members</span>}
        </div>
        <TransactionList budget={budget} fetchBudgets={fetchBudgets} transactions={budget.incomes} type="income"/>
        <TransactionList budget={budget} fetchBudgets={fetchBudgets} transactions={budget.expenses} type="expense"/>
      </>
    )}
    </>
  )
}

export default BudgetListItem;