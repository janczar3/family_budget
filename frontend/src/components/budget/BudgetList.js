import React from 'react';
import BudgetListItem from "./BudgetListItem";

function BudgetList({budgets, nextPage, previousPage, setCurrentPage, handleDeleteBudget, fetchBudgets}) {

  return (
    <div>
      <h2>Budget List</h2>
      <ul>
        {budgets.map((budget) => (
          <li key={budget.id}>
            <BudgetListItem budget={budget} handleDeleteBudget={handleDeleteBudget} fetchBudgets={fetchBudgets}/>
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
