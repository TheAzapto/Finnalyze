// src/services/mongodb.js
// Fetch data from the Vercel serverless API endpoints

/**
 * Market page: fetch from /api/market
 */
export async function fetchMarketData() {
    const res = await fetch('/api/market');
    if (!res.ok) throw new Error('Failed to fetch market data');
    return res.json();
}

/**
 * News page: fetch from /api/news
 */
export async function fetchNewsData() {
    const res = await fetch('/api/news');
    if (!res.ok) throw new Error('Failed to fetch news data');
    return res.json();
}

/**
 * Sentiment page: fetch from /api/sentiment?company=...
 */
export async function fetchSentimentData(company) {
    const url = company ? `/api/sentiment?company=${encodeURIComponent(company)}` : '/api/sentiment';
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch sentiment data');
    return res.json();
}
