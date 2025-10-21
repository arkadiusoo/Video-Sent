import React from "react";

function ResultView({ result }) {
  return (
    <div>
      <h3>Wynik analizy:</h3>
      <p><b>Link:</b> {result.link}</p>
      <p><b>Transkrypcja:</b> {result.transcript}</p>
      <p><b>Sentyment:</b> {result.sentiment}</p>
    </div>
  );
}

export default ResultView;
