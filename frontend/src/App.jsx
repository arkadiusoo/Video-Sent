import React, { useState } from "react";
import { analyzeVideo } from "./api";
import InputLink from "./components/InputLink";
import ResultView from "./components/ResultView";

function App() {
  const [result, setResult] = useState(null);

  const handleSubmit = async (link) => {
    const data = await analyzeVideo(link);
    setResult(data);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h2>Video-Sent MVP</h2>
      <InputLink onSubmit={handleSubmit} />
      {result && <ResultView result={result} />}
    </div>
  );
}

export default App;
