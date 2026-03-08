// src/pages/MarketPage.jsx
import React, { useEffect, useState } from "react";
import { fetchMarketData } from "../services/mongodb";
import { SkeletonTable } from "../components/Skeleton";

const MarketPage = () => {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchMarketData();
        setRows(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load market data.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="page-shell page-transition">
      <header className="header">
        <h1>Live Market Overview</h1>
        <p>Snapshot of key indices and benchmarks powered by MongoDB Atlas.</p>
      </header>

      <section className="results-panel">
        <h2>Global Indices</h2>

        {loading && <SkeletonTable rows={8} cols={5} />}
        {error && <div className="error-box">{error}</div>}

        {!loading && !error && (
          <table className="results-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Name</th>
                <th>Price</th>
                <th>Change</th>
                <th>Change %</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.symbol}</td>
                  <td>{row.name}</td>
                  <td>{row.price}</td>
                  <td className={row.change >= 0 ? "score-positive" : "score-negative"}>
                    {row.change.toFixed(2)}
                  </td>
                  <td className={row.changePercent >= 0 ? "score-positive" : "score-negative"}>
                    {row.changePercent.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
};

export default MarketPage;
