import React from "react";
import styled from "styled-components";

export default ({ id, balance, numTransactions }) => {
  return (
    <WalletContainer>
      <h3>Your Wallet</h3>
      <p>ID: {id ? id : "ID NOT SET"}</p>
      <p>Balance: {id ? balance : "N/A"}</p>
      <p>Total transactions: {id ? numTransactions : "N/A"}</p>
    </WalletContainer>
  );
};

const WalletContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;
