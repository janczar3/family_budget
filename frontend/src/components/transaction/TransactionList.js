import React from "react";
import TransactionForm from "../transaction/TransactionForm";

function TransactionList({budget, fetchBudgets, transactions, type}) {
  return (
    <div style={{width: 300, border: "1px solid black", margin: 10}}>
      {transactions.length ? (
        <>
          <div>
            <p>{type}:</p>
            <ul>
              {transactions.map((transaction) => (
                <li key={transaction.id}>
                  <p>{transaction.name}</p>
                  <p>{transaction.category}</p>
                  <p>{transaction.value}</p>
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