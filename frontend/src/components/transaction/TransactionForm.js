import React, { useState } from 'react';
import Select from 'react-select';

import {IncomeCategory, ExpenseCategory} from "../../constants";
import {createIncome, createExpense} from "../../services/transaction";

function TransactionForm({budget, fetchBudgets, type, edit=false}) {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const categories = {
    expense: [
      {value: IncomeCategory.GROCERIES, label: IncomeCategory.GROCERIES},
      {value: IncomeCategory.RESTAURANT, label: IncomeCategory.RESTAURANT},
      {value: IncomeCategory.ENTERTAINMENT, label: IncomeCategory.ENTERTAINMENT},
      {value: IncomeCategory.HOME, label: IncomeCategory.HOME},
      {value: IncomeCategory.MEDICINES, label: IncomeCategory.MEDICINES},
      {value: IncomeCategory.CHILDREN, label: IncomeCategory.CHILDREN},
      {value: IncomeCategory.INVESTMENTS, label: IncomeCategory.INVESTMENTS},
      {value: IncomeCategory.PETS, label: IncomeCategory.PETS},
      {value: IncomeCategory.CAR, label: IncomeCategory.CAR},
      {value: IncomeCategory.BILL, label: IncomeCategory.BILL},
      {value: IncomeCategory.OTHER, label: IncomeCategory.OTHER},
    ],
    income: [
      {value: ExpenseCategory.SALARY, label: ExpenseCategory.SALARY},
      {value: ExpenseCategory.SAVINGS, label: ExpenseCategory.SAVINGS},
      {value: ExpenseCategory.OTHER, label: ExpenseCategory.OTHER},
    ]
  };

  const apiMethods = {
    income: {
      create: createIncome,
    },
    expense: {
      create: createExpense,
    }
  };

  const handleSelectCategory = (selectedOption) => {
    setCategory(selectedOption);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const data = {
        name: name,
        category: category.value,
        value: amount,
        budget: budget.id,
      };
      await apiMethods[type].create(data);
      setName('');
      setCategory('');
      setAmount(0);
      setSuccess(true);
      await fetchBudgets();
    } catch (err) {
      setError(err);
    }
  };

  return (
    <div style={{width: 150, border: "1px solid black"}}>
      {edit ? (
        <p>Edit {type}</p>
      ): (
        <p>Add New {type}</p>
      )}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <br/>
          <label htmlFor="category">category</label>
          <Select
            value={category}
            onChange={handleSelectCategory}
            options={categories[type]}
            placeholder="Select category"
          />
          <label htmlFor="name">Amount</label>
          <input
            type="number"
            id="amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            step="0.01"
            min="0"
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {success && <p>Success!</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}

export default TransactionForm;
