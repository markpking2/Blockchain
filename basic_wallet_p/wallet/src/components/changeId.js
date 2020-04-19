import React, { useState } from "react";
import styled from "styled-components";
import axios from "axios";

export default ({ id, setId, changeId }) => {
  return (
    <ChangeIdContainer>
      <h3>Change ID</h3>
      <form onSubmit={changeId}>
        <input
          value={id}
          onChange={e => setId(e.target.value)}
          placeholder='Enter ID'
        />
        <button type='submit'>Change</button>
      </form>
    </ChangeIdContainer>
  );
};

const ChangeIdContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;
