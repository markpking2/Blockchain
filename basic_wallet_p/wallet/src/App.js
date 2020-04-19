import React, { useState, useEffect } from "react";
import { ChangeId, Wallet, AddTransaction, Transaction } from "./components";
import axios from "axios";
import styled from "styled-components";

function App() {
  const [id, setId] = useState("");
  const [state, setState] = useState({
    id: "",
    balance: 0,
    transactions: [],
    idTransactions: []
  });

  useEffect(() => {
    if (state.transactions.length == 0) {
      getTransactions();
    }
  });

  useEffect(() => {
    const idTransactions = state.transactions.filter(
      t => t.sender == state.id || t.recipient == state.id
    );
    const balance =
      idTransactions
        .filter(t => t.recipient == state.id)
        .reduce((acc, t) => acc + t.amount, 0) -
      idTransactions
        .filter(t => t.sender == state.id)
        .reduce((acc, t) => acc + t.amount, 0);
    setState({
      ...state,
      idTransactions,
      balance,
      totalTransactions: idTransactions.length
    });
  }, [state.id, state.transactions]);

  const changeId = e => {
    e.preventDefault();
    try {
      if (id.length > 0) {
        setState({ ...state, id });
      } else {
        throw "Id field must not be empty.";
      }
    } catch (err) {
      console.log(err);
    }
  };

  function getTransactions() {
    axios
      .get("http://localhost:5000/chain")
      .then(({ data: { chain } }) => {
        setState({
          ...state,
          transactions: chain.map(block => block.transactions).flat()
        });
      })
      .catch(err => {
        console.log(err);
      });
  }

  return (
    <div>
      <StyledHeader>
        <h1>Blockchain Wallet</h1>
        <button
          onClick={() => {
            getTransactions();
          }}
        >
          Get Transactions
        </button>
      </StyledHeader>
      <StyledDiv>
        <ChangeId id={id} setId={setId} changeId={changeId} />
        <Wallet
          id={state.id}
          balance={state.balance}
          numTransactions={state.idTransactions.length}
        />
        <AddTransaction />
      </StyledDiv>
      <h4>Your Transactions:</h4>
      {state.id ? (
        state.idTransactions.map(t => (
          <Transaction
            recipient={t.recipient}
            sender={t.sender}
            amount={t.amount}
            id={state.id}
          />
        ))
      ) : (
        <p>N/A</p>
      )}
    </div>
  );
}

export default App;

const StyledHeader = styled.header`
  display: flex;
  text-align: center;
  align-items: center;
  background-color: grey;
  padding: 1rem;
  h1 {
    padding: 0;
    width: 100%;
  }

  button {
    height: 50px;
    background-color: black;
    color: white;
    border-radius: 50%;
  }
`;

const StyledDiv = styled.div`
  display: flex;
  justify-content: center;
  div {
    width: 33%;
    height: 250px;
    border: 1px solid black;
  }
`;
