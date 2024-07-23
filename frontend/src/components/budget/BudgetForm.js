import React, { useState } from 'react';
import { createBudget } from "../../services/budget";

function BudgetForm({fetchBudgets, edit=false}) {
  const [name, setName] = useState('');
  const [users, setUsers] = useState('');
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
      if (users) {
        data.users = users.split(',');
      }
      await createBudget(data);
      setName('');
      setUsers('');
      setSuccess(true);
      await fetchBudgets();
    } catch (err) {
      setError(err);
    }
  };

  return (
    <div>
      {edit ? (
        <h2>Edit Budget</h2>
      ): (
        <h2>Add New Budget</h2>
      )}
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <label htmlFor="name">Budget Name</label>
          <br/>
          <input
            type="text"
            id="users"
            value={users}
            onChange={(e) => setUsers(e.target.value)}
          />
          <label htmlFor="name">Share budget with users (ex. "john123,bob242")</label>
        </div>
        <button type="submit">Submit</button>
      </form>
      {success && <p>Success!</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}

export default BudgetForm;
