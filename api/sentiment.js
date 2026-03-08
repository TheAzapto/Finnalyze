// api/sentiment.js — GET /api/sentiment?company=...
const { getDb } = require('./_db');

module.exports = async function handler(req, res) {
    try {
        const db = await getDb();
        const col = db.collection('stockData');
        const company = req.query.company;

        let filter = {};
        if (company) {
            filter = {
                $or: [
                    { code: company },
                    { name: { $regex: company, $options: 'i' } },
                ],
            };
        }

        const docs = await col.find(filter).limit(1000).toArray();

        const out = docs.map((d) => {
            let impact = 0;
            try { impact = Number(d.impact_score || 0) || 0; } catch { impact = 0; }
            return {
                code: d.code || d.symbol || String(d._id),
                name: d.name || '',
                prediction: d.prediction || null,
                impact_score: impact,
                latest_headline: d.latest_headline || d.title || null,
                latest_article: d.latest_article || d.article || d.summary || null,
            };
        });

        res.json(out);
    } catch (err) {
        console.error('Sentiment API error:', err);
        res.status(500).json({ error: 'Failed to fetch sentiment data' });
    }
};
