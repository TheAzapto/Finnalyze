from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import os
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, origins="*")

# MongoDB connection (server-side). Prefer setting MONGO_URI in environment for security.
MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://root:1234@cluster0.260lmcy.mongodb.net/'
MONGO_DB = os.environ.get('MONGO_DB') or 'Finnalyze'
try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB]
except Exception as e:
    print('Warning: could not connect to MongoDB:', e)
    mongo_client = None
    mongo_db = None


@app.route('/mongo/debug', methods=['GET'])
def mongo_debug():
    """Return basic diagnostics: connection status, collection list and counts.
    Helps verify whether documents exist and whether the filter is excluding them.
    """
    if mongo_db is None:
        return jsonify({'ok': False, 'error': 'MongoDB not connected on server'}), 500

    try:
        cols = mongo_db.list_collection_names()
        info = {'ok': True, 'collections': cols}

        def counts_for(colname):
            col = mongo_db.get_collection(colname)
            total = col.count_documents({})
            filtered = col.count_documents({'prediction': {'$ne': None, '$exists': True, '$nin': ['down']}})
            return {'total': total, 'filtered': filtered}

        # Check common collections
        if 'stockData' in cols:
            info['stockData'] = counts_for('stockData')
        if 'news' in cols:
            info['news'] = counts_for('news')

        return jsonify(info), 200
    except Exception as e:
        print('Mongo debug error:', e)
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route("/market", methods=["GET"])
def market_overview():
    # choose a larger set of tickers/indices to populate the market table
    symbols = [
        # US indices
        "^GSPC",   # S&P 500
        "^DJI",    # Dow 30
        "^IXIC",   # Nasdaq
        # Indian indices
        "^NSEI",   # Nifty 50
        "^BSESN",  # BSE Sensex
        # Large Indian stocks (NSE suffix)
        "RELIANCE.NS",
        "TCS.NS",
        "HDFCBANK.NS",
        "INFY.NS",
        "ICICIBANK.NS",
        "LT.NS",
        "ITC.NS",
        "SBIN.NS",
        "KOTAKBANK.NS",
        "AXISBANK.NS",
        "BHARTIARTL.NS",
        "HINDUNILVR.NS",
        "BAJFINANCE.NS",
        "MARUTI.NS",
        "ONGC.NS",
        "POWERGRID.NS",
        "TITAN.NS",
        "ULTRACEMCO.NS",
        "M&M.NS",
        "SUNPHARMA.NS",
        # Additional international/sector tickers
        "^FTSE",
        "^STOXX50E",
        "^N225",
    ]

    tickers = yf.Tickers(" ".join(symbols))
    rows = []

    for sym in symbols:
        info = tickers.tickers[sym].info
        price = info.get("regularMarketPrice")
        prev_close = info.get("regularMarketPreviousClose")
        if price is None or prev_close is None:
            continue

        change = price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close else 0

        rows.append({
            "symbol": sym,
            "name": info.get("shortName", sym),
            "price": float(price),
            "change": float(change),
            "changePercent": float(change_percent),
        })

    return jsonify(rows), 200

SAMPLE_INDIAN_NEWS = [
    {
        "title": "Nifty 50 ends higher led by banking and IT stocks",
        "url": "https://www.nseindia.com/",
        "source": "Sample – Indian Markets",
        "published": "2025-11-27 15:30",
        "summary": "Benchmark indices closed in the green with banking and IT heavyweights driving gains amid positive global cues."
    },
    {
        "title": "Sensex climbs as Reliance and HDFC Bank rally",
        "url": "https://www.bseindia.com/",
        "source": "Sample – Indian Markets",
        "published": "2025-11-27 14:10",
        "summary": "Reliance Industries and HDFC Bank led a broad-based rally on Dalal Street as investors added positions in large caps."
    },
    {
        "title": "RBI policy expectations keep traders cautious on PSU banks",
        "url": "https://www.rbi.org.in/",
        "source": "Sample – Indian Markets",
        "published": "2025-11-26 11:05",
        "summary": "PSU bank stocks saw rangebound moves as traders awaited clarity on RBI’s stance on liquidity and rates."
    },
    {
        "title": "IT stocks rebound on strong US tech earnings",
        "url": "https://www.moneycontrol.com/",
        "source": "Sample – Indian Markets",
        "published": "2025-11-25 10:20",
        "summary": "Indian IT majors gained after upbeat guidance from global technology peers lifted sentiment on export-focused companies."
    },
]

@app.route("/market-news", methods=["GET"])
def market_news():
    # For the project/demo we serve a stable sample feed.
    # In a real deployment this would call a reliable news API.
    return jsonify(SAMPLE_INDIAN_NEWS), 200


@app.route('/mongo/market', methods=['GET'])
def mongo_market():
    """Return market documents from MongoDB `stockData` collection.
    Filters out documents where `prediction` is null or equal to 'down'.
    """
    if mongo_db is None:
        return jsonify({'error': 'MongoDB not available on server'}), 500

    col = mongo_db.get_collection('stockData')
    try:
        # Include documents where prediction is null/missing, but exclude explicit 'down'
        cursor = col.find({'prediction': {'$ne': 'down'}})
        docs = list(cursor.limit(500))
    except Exception as e:
        print('Mongo query error:', e)
        return jsonify({'error': str(e)}), 500

    rows = []
    for d in docs:
        rows.append({
            'symbol': d.get('code') or d.get('symbol') or str(d.get('_id')),
            'name': d.get('name') or '',
            'price': float(d.get('price') or d.get('latest_price') or 0),
            'change': float(d.get('change') or 0),
            'changePercent': float(d.get('changePercent') or d.get('change_percent') or 0),
        })

    return jsonify(rows), 200


@app.route('/mongo/news', methods=['GET'])
def mongo_news():
    """Return news-like documents from MongoDB. Uses `news` collection if present,
    otherwise falls back to `stockData`.
    Filters out documents where `prediction` is null or equal to 'down'.
    """
    if mongo_db is None:
        return jsonify({'error': 'MongoDB not available on server'}), 500

    collection_name = 'news' if 'news' in mongo_db.list_collection_names() else 'stockData'
    col = mongo_db.get_collection(collection_name)
    try:
        # Include documents where prediction is null/missing, but exclude explicit 'down'
        cursor = col.find({'prediction': {'$ne': 'down'}})
        docs = list(cursor.limit(500))
    except Exception as e:
        print('Mongo query error:', e)
        return jsonify({'error': str(e)}), 500

    articles = []
    for d in docs:
        articles.append({
            'title': d.get('latest_headline') or d.get('title') or d.get('name') or '',
            'url': d.get('url') or d.get('link') or '#',
            'source': d.get('source') or d.get('source_name') or '',
            'published': d.get('updated_at') or d.get('created_at') or d.get('published') or None,
            'summary': d.get('latest_article') or d.get('summary') or d.get('description') or '',
        })

    return jsonify(articles), 200


@app.route('/mongo/sentiment', methods=['GET'])
def mongo_sentiment():
    """Return sentiment/impact_score data from stockData.
    Optional query param `company` filters by code (exact) or name (case-insensitive substring).
    """
    if mongo_db is None:
        return jsonify({'error': 'MongoDB not available on server'}), 500

    company = request.args.get('company')
    col = mongo_db.get_collection('stockData')
    try:
        if company:
            # try matching code exactly first, then name substring (case-insensitive)
            filt = {'$or': [{'code': company}, {'name': {'$regex': company, '$options': 'i'}}]}
        else:
            filt = {}

        cursor = col.find(filt).limit(1000)
        docs = list(cursor)
    except Exception as e:
        print('Mongo sentiment query error:', e)
        return jsonify({'error': str(e)}), 500

    out = []
    for d in docs:
        try:
            impact = float(d.get('impact_score', 0) or 0)
        except Exception:
            # if it's not convertible, set 0
            impact = 0.0

        out.append({
            'code': d.get('code') or d.get('symbol') or str(d.get('_id')),
            'name': d.get('name') or '',
            'prediction': d.get('prediction'),
            'impact_score': impact,
            'latest_headline': d.get('latest_headline') or d.get('title') or None,
            'latest_article': d.get('latest_article') or d.get('article') or d.get('summary') or None,
        })

    return jsonify(out), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

