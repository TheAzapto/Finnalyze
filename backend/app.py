from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from FinLlama_Middleware import Evaluate
import requests
from bs4 import BeautifulSoup
import yfinance as yf

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        article = request.json.get('article')
        if not article:
            return jsonify({'error': 'Article is required'}), 400
        
        impact_score = Evaluate(article)
        # impact_score = float(impact_score)
        # result = json.load({"impact_score": impact_score})
        
        print(impact_score)

        return impact_score, 200
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route("/market", methods=["GET"])
def market_overview():
    # choose some indices (you can change to NIFTY/BSE etc)
    symbols = [
        "^GSPC",   # S&P 500
        "^DJI",    # Dow 30
        "^IXIC",   # Nasdaq
        "^NSEI",   # Nifty 50
        "^BSESN",  # BSE Sensex
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
