import React, { useState } from 'react';
import { createBudget } from "../../services/budget";

function BudgetForm({fetchBudgets}) {
  const [name, setName] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const data = {
        name: name,
      };
      await createBudget(data);
      setName('');
      setSuccess(true);
      await fetchBudgets();
    } catch (err) {
      setError(err);
    }
  };

  return (
    <div>
      <h2>Add New Budget</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Budget Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add Budget</button>
      </form>
      {success && <p>Budget added successfully!</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}

export default BudgetForm;
