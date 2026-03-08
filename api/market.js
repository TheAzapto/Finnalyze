// api/market.js — GET /api/market
const { getDb } = require('./_db');

module.exports = async function handler(req, res) {
    try {
        const db = await getDb();
        const col = db.collection('stockData');
        const docs = await col.find({ prediction: { $ne: 'down' } }).limit(500).toArray();

        const rows = docs.map((d) => ({
            symbol: d.code || d.symbol || String(d._id),
            name: d.name || '',
            price: Number(d.price || d.latest_price || 0),
            change: Number(d.change || 0),
            changePercent: Number(d.changePercent || d.change_percent || 0),
        }));

        res.json(rows);
    } catch (err) {
        console.error('Market API error:', err);
        res.status(500).json({ error: 'Failed to fetch market data' });
    }
};
