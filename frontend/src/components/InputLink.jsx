import React, { useState } from "react";

function InputLink({ onSubmit }) {
  const [link, setLink] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (link.trim()) onSubmit(link);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
      <input
        type="text"
        placeholder="Wklej link do filmu..."
        value={link}
        onChange={(e) => setLink(e.target.value)}
        style={{ width: "60%", padding: "0.5rem" }}
      />
      <button type="submit" style={{ marginLeft: "0.5rem", padding: "0.5rem" }}>
        Analizuj
      </button>
    </form>
  );
}

export default InputLink;
