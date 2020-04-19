import React, { useState } from "react";
import styled from "styled-components";
import axios from "axios";

export default ({ id, setId, changeId }) => {
  const [sender, setSender] = useState("");
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");

  const addTransaction = async () => {
    try {
      if (sender && recipient && amount > 0) {
        const response = await axios.post(
          "http://localhost:5000/transactions/new",
          { sender, recipient, amount: parseInt(amount) }
        );
        console.log(response);
      } else {
        throw "Invalid Transaction!";
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <AddTransactionContainer>
      <h3>Add Transaction</h3>
      <StyledForm
        onSubmit={e => {
          e.preventDefault();
          addTransaction().then(() => {});
        }}
      >
        <input
          value={sender}
          onChange={e => setSender(e.target.value)}
          placeholder='Sender'
        />
        <input
          value={recipient}
          onChange={e => setRecipient(e.target.value)}
          placeholder='Recipient'
        />
        <input
          value={amount}
          onChange={e => setAmount(e.target.value)}
          placeholder='Amount'
        />
        <button type='submit'>Add</button>
      </StyledForm>
    </AddTransactionContainer>
  );
};

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  input,
  button {
    width: 50%;
  }
`;

const AddTransactionContainer = styled.div`
  text-align: center;
`;
