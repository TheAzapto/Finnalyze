// api/news.js — GET /api/news
const { getDb } = require('./_db');

module.exports = async function handler(req, res) {
    try {
        const db = await getDb();
        const collections = await db.listCollections().toArray();
        const colNames = collections.map((c) => c.name);
        const colName = colNames.includes('news') ? 'news' : 'stockData';
        const col = db.collection(colName);

        const docs = await col.find({ prediction: { $ne: 'down' } }).limit(500).toArray();

        const articles = docs.map((d) => ({
            title: d.latest_headline || d.title || d.name || '',
            url: d.url || d.link || '#',
            source: d.source || d.source_name || '',
            published: d.updated_at || d.created_at || d.published || null,
            summary: d.latest_article || d.summary || d.description || '',
        }));

        res.json(articles);
    } catch (err) {
        console.error('News API error:', err);
        res.status(500).json({ error: 'Failed to fetch news' });
    }
};
