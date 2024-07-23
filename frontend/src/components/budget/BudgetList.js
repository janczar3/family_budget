import React, {useState} from 'react';
import TransactionList from "../transaction/TransactionList";

function BudgetList({budgets, nextPage, previousPage, setCurrentPage, handleDeleteBudget}) {
  const [budgetsShowDetails, setBudgetsShowDetails] = useState([]);

  const toggleBudgetDetails = (id) => {
    if (budgetsShowDetails.includes(id)) {
      setBudgetsShowDetails(budgetsShowDetails.filter(budgetId => budgetId !== id));
    } else {
      setBudgetsShowDetails([...budgetsShowDetails, id]);
    }
  };

  return (
    <div>
      <h2>Budget List</h2>
      <ul>
        {budgets.map((budget) => (
          <li key={budget.id}>
            <a href="#" onClick={() => toggleBudgetDetails(budget.id)}>{budget.name} </a>
            <button onClick={() => handleDeleteBudget(budget.id)}>delete</button>
            {budgetsShowDetails.includes(budget.id) && (
              <>
                <div>
                  <p>Budget members:</p>
                  <ul>
                    {budget.user_names.map((username) => (
                    <li key={username}>{username}</li>
                    ))}
                  </ul>
                </div>
                <TransactionList transactions={budget.incomes} type="incomes"/>
                <TransactionList transactions={budget.expenses} type="expenses"/>
              </>
            )}
          </li>
        ))}
      </ul>
      <div style={{margin: 'auto'}}>
        {previousPage && (
          <button
            onClick={() => setCurrentPage(previousPage)}
          >
            &lt;
          </button>
        )}
        {nextPage && (
          <button
            onClick={() => setCurrentPage(nextPage)}
          >
            &gt;
          </button>
        )}
      </div>
    </div>
  );
}

export default BudgetList;
