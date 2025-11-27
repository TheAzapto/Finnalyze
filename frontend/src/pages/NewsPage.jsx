import React, { useEffect, useState } from "react";
import axios from "axios";

function NewsPage() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const res = await axios.get("http://localhost:5000/market-news");
        setArticles(res.data || []);
      } catch (err) {
        console.error(err);
        setArticles([]);
      } finally {
        setLoading(false);
      }
    };
    fetchNews();
  }, []);

  return (
    <div className="page-root">
      <h1>Market News</h1>
      <p>Latest headlines from Yahoo Finance / sample feed.</p>

      {loading && <p className="placeholder">Loading news...</p>}

      {!loading && !articles.length && (
        <p className="placeholder">No news available right now.</p>
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
            <a
              href={article.url}
              target="_blank"
              rel="noreferrer"
              className="news-link"
            >
              Read article →
            </a>
          </article>
        ))}
      </div>
    </div>
  );
}

export default NewsPage;
