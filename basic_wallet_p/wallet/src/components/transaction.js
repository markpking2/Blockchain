import React from "react";

export default ({ recipient, sender, amount, id }) => {
  return (
    <div>
      <span style={recipient == id ? { color: "green" } : { color: "red" }}>
        Sender: {sender} Recipient: {recipient} Amount: {amount}
      </span>
    </div>
  );
};
