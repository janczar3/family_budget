import React from "react";

function TransactionList({transactions, type}) {
  return (
    <div>
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
      ) : <p>no {type}</p>}
    </div>
  );
}

export default TransactionList;