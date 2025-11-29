// src/pages/SentimentPage.jsx
import React, { useState } from "react";
import api from "../api/backend";
import "../App.css";

const SentimentPage = () => {
  const [company, setCompany] = useState("");
  const [results, setResults] = useState([]);
  const [selectedDetail, setSelectedDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch sentiment scores from backend Mongo proxy. If `company` is provided,
  // query for that company only, otherwise fetch all.
  const fetchSentiment = async (companyFilter = "") => {
    setError("");
    setResults([]);
    setSelectedDetail(null);
    setLoading(true);
    try {
      const url = companyFilter
        ? `/mongo/sentiment?company=${encodeURIComponent(companyFilter)}`
        : `/mongo/sentiment`;
      const res = await api.get(url);
      const data = res.data || [];
      setResults(data);
      // If a company filter was used, auto-select the first returned detail
      if (companyFilter && data.length > 0) setSelectedDetail(data[0]);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Failed to load sentiment data from server.");
    } finally {
      setLoading(false);
    }
  };

  // NOTE: Do not fetch on mount. Only fetch when user explicitly searches.

  const formatScore = (score) =>
    typeof score === "number" ? score.toFixed(2) : score;

  const getScoreClass = (score) => {
    if (score > 0.2) return "score-positive";
    if (score < -0.2) return "score-negative";
    return "score-neutral";
  };

  const handleSearch = () => {
    if (!company.trim()) {
      setError("Please enter a company name or ticker before searching.");
      return;
    }
    // clear any previous error and fetch for the entered company only
    setError("");
    fetchSentiment(company.trim());
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
          <button onClick={handleSearch} disabled={loading}>
            {loading ? "Loading..." : "Search"}
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
            <div>
              <table className="results-table">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Impact Score</th>
                    <th>Prediction</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((row, idx) => (
                    <tr
                      key={idx}
                      onClick={() => setSelectedDetail(row)}
                      style={{ cursor: "pointer" }}
                    >
                      <td>{row.name || row.code || row.company || "-"}</td>
                      <td className={getScoreClass(row.impact_score)}>
                        {row.impact_score === 0 ? "No score" : formatScore(row.impact_score)}
                      </td>
                      <td>{row.prediction || "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {selectedDetail && (
                <div className="detail-card" style={{ marginTop: 16 }}>
                  <h3>{selectedDetail.name || selectedDetail.code}</h3>
                  <p>
                    <strong>Code:</strong> {selectedDetail.code || "-"} &nbsp; 
                    <strong>Prediction:</strong> {selectedDetail.prediction || "-"} &nbsp; 
                    <strong>Impact:</strong>{" "}
                    {selectedDetail.impact_score === 0 ? (
                      <em>No score</em>
                    ) : (
                      <span className={getScoreClass(selectedDetail.impact_score)}>
                        {formatScore(selectedDetail.impact_score)}
                      </span>
                    )}
                  </p>

                  <div style={{ marginTop: 8 }}>
                    <h4>Headline</h4>
                    <p>{selectedDetail.latest_headline || "No headline available."}</p>
                  </div>

                  <div style={{ marginTop: 8 }}>
                    <h4>Article / Summary</h4>
                    <div className="article-text" style={{ maxHeight: 260, overflowY: "auto", whiteSpace: "pre-wrap" }}>
                      {selectedDetail.latest_article || "No article text available in the database."}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </>
  );
};

export default SentimentPage;
