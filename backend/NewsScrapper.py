import json
import yfinance as yf
import requests
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb+srv://root:1234@cluster0.260lmcy.mongodb.net/')
db = client['Finnalyze']
collection = db['stockData']


with open('backend\stockList.json', 'r') as f:
    stockList = json.load(f)

while True:
    try:
        for stock in stockList:
            stockCode = stock['code'] + '.NS'
            news = yf.Ticker(stockCode).get_news()
        
            for article in news:
                content = article['content']['summary']
                title = article['content']['title']
            
                response = requests.post(
                    'http://localhost:5000/evaluate',
                    json={"article": content}
                    )

                impact_score = float(response.json())

                updates = {
                    "prediction" : 'down' if impact_score < 0 else 'up',
                    "latest_headline": title,
                    "latest_article": content,
                    "updated_at": datetime.datetime.utcnow()
                }
    
                result = collection.update_one(
                    {"code": stockCode.replace('.NS', '')},
                    {"$set": updates}
                )
                
    except KeyboardInterrupt as e:
        break

    except Exception as e:
        print(e)
        continue