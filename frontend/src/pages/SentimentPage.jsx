// src/pages/SentimentPage.jsx
import React, { useState } from "react";
import api from "../api/backend";
import "../App.css";

const SentimentPage = () => {
  const [company, setCompany] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setError("");
    setResults([]);

    if (!company.trim()) {
      setError("Please enter a company name or ticker.");
      return;
    }

    try {
      setLoading(true);
      const res = await api.post("/analyze", { company: company.trim() });
      setResults(res.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error ||
          "Something went wrong while analyzing. Check if backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatScore = (score) =>
    typeof score === "number" ? score.toFixed(2) : score;

  const getScoreClass = (score) => {
    if (score > 0.2) return "score-positive";
    if (score < -0.2) return "score-negative";
    return "score-neutral";
  };

  return (
    <>
      <header className="header">
        <h1>Market Sentiment Analyzer</h1>
        <p>
          Enter a company name or ticker to analyze news-driven sentiment using
          an LLM-based model.
        </p>
      </header>

      <main className="main-layout">
        <section className="input-panel">
          <h2>Company</h2>
          <input
            type="text"
            placeholder="e.g., HDFC Bank, Reliance, TCS"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze News Sentiment"}
          </button>
          {error && <div className="error-box">{error}</div>}
        </section>

        <section className="results-panel">
          <h2>Impact Scores</h2>
          {!results.length && !loading && !error && (
            <p className="placeholder">
              Results will appear here after you run an analysis.
            </p>
          )}

          {results.length > 0 && (
            <table className="results-table">
              <thead>
                <tr>
                  <th>Company</th>
                  <th>Impact Score</th>
                </tr>
              </thead>
              <tbody>
                {results.map((row, idx) => (
                  <tr key={idx}>
                    <td>{row.company}</td>
                    <td className={getScoreClass(row.impact_score)}>
                      {formatScore(row.impact_score)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </>
  );
};

export default SentimentPage;
