import React from "react";
import TransactionForm from "../transaction/TransactionForm";

function TransactionList({budget, fetchBudgets, transactions, type}) {
  return (
    <div style={{width: 300, border: "1px solid black", margin: 10, padding: 10}}>
      {transactions.length ? (
        <>
          <div style={{margin: 10}}>
            <h4>{type}s:</h4>
            <ul>
              {transactions.map((transaction) => (
                <li key={transaction.id}>
                  <span>{transaction.name}</span>
                  <ul>
                    <li>category: {transaction.category}</li>
                    <li>amount: {transaction.value}</li>
                  </ul>
                </li>
              ))}
            </ul>
          </div>
        </>
      ) : <p>no {type}s</p>}
      <TransactionForm budget={budget} fetchBudgets={fetchBudgets} type={type}/>
    </div>
  );
}

export default TransactionList;