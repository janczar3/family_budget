import React from 'react';

function BudgetList({budgets, nextPage, previousPage, setCurrentPage, handleDeleteBudget}) {
  return (
    <div>
      <h2>Budget List</h2>
      <ul>
        {budgets.map((budget) => (
          <li key={budget.id}>
            <span>{budget.name} </span>
            <a href="#" onClick={() => handleDeleteBudget(budget.id)}>Delete</a>
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
