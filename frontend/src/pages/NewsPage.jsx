// src/pages/NewsPage.jsx
import React, { useEffect, useState } from "react";
import { fetchNewsData } from "../services/mongodb";
import { SkeletonNewsGrid } from "../components/Skeleton";

// Static fallback if MongoDB returns nothing
const SAMPLE_NEWS = [
  {
    title: "Nifty 50 ends higher led by banking and IT stocks",
    url: "https://www.nseindia.com/",
    source: "Sample – Indian Markets",
    published: "2025-11-27 15:30",
    summary:
      "Benchmark indices closed in the green with banking and IT heavyweights driving gains amid positive global cues.",
  },
  {
    title: "Sensex climbs as Reliance and HDFC Bank rally",
    url: "https://www.bseindia.com/",
    source: "Sample – Indian Markets",
    published: "2025-11-27 14:10",
    summary:
      "Reliance Industries and HDFC Bank led a broad-based rally on Dalal Street as investors added positions in large caps.",
  },
  {
    title: "RBI policy expectations keep traders cautious on PSU banks",
    url: "https://www.rbi.org.in/",
    source: "Sample – Indian Markets",
    published: "2025-11-26 11:05",
    summary:
      "PSU bank stocks saw rangebound moves as traders awaited clarity on RBI's stance on liquidity and rates.",
  },
  {
    title: "IT stocks rebound on strong US tech earnings",
    url: "https://www.moneycontrol.com/",
    source: "Sample – Indian Markets",
    published: "2025-11-25 10:20",
    summary:
      "Indian IT majors gained after upbeat guidance from global technology peers lifted sentiment on export-focused companies.",
  },
];

function NewsPage() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchNewsData();
        setArticles(data.length > 0 ? data.slice(0, 20) : SAMPLE_NEWS);
      } catch (err) {
        console.error(err);
        setArticles(SAMPLE_NEWS);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="page-root page-transition">
      <header className="header">
        <h1>Market News</h1>
        <p>Latest headlines from the financial world</p>
      </header>

      {loading && <SkeletonNewsGrid count={6} />}

      {!loading && !articles.length && (
        <p className="placeholder" style={{ textAlign: "center" }}>
          No news available right now.
        </p>
      )}

      <div className="news-grid">
        {articles.map((article, idx) => (
          <article key={idx} className="news-card">
            <div className="news-meta">
              <span className="news-source">
                {article.source || "Yahoo Finance"}
              </span>
              {article.published && (
                <span className="news-time">{article.published}</span>
              )}
            </div>
            <h3>{article.title}</h3>
            {article.summary && (
              <p className="news-summary">{article.summary}</p>
            )}
          </article>
        ))}
      </div>
    </div>
  );
}

export default NewsPage;
