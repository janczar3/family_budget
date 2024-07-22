import React, {useEffect, useState} from 'react';
import BudgetList from "./BudgetList";
import BudgetForm from "./BudgetForm";
import {listBudgets, deleteBudget} from "../../services/budget";
function BudgetPanel() {
  const [budgets, setBudgets] = useState([]);
  const [error, setError] = useState(null);
  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [currentPage, setCurrentPage] = useState(null);

  useEffect(() => {
    fetchBudgets(currentPage);
  }, [currentPage]);

  const fetchBudgets = async () => {
    try {
      const response = await listBudgets(currentPage);
      setBudgets(response.data.results);
      setNextPage(response.data.next);
      setPreviousPage(response.data.previous);
    } catch (err) {
      setError(err);
    }
  };

  const handleDeleteBudget = async (id) => {
    try {
      await deleteBudget(id);
      await fetchBudgets();
    } catch (err) {
      setError(err);
    }
  };

  if (error) return <div>Error: {error.message}</div>;
  return (
    <div className="BudgetPanel">
      <BudgetList
        budgets={budgets}
        nextPage={nextPage}
        previousPage={previousPage}
        setCurrentPage={setCurrentPage}
        handleDeleteBudget={handleDeleteBudget}
      />
      <BudgetForm fetchBudgets={fetchBudgets}/>
    </div>
  );
}

export default BudgetPanel;
