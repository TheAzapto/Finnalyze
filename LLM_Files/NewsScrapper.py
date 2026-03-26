import json
import yfinance as yf
import datetime
from pymongo import MongoClient
from FinLlama_Middleware import Evaluate
from time import sleep
import os
from predictor import get_prediction
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['Finnalyze']
collection = db['stockData']


with open(os.path.join(os.getcwd(), r'stockList.json'), 'r') as f:
    stockList = json.load(f)

while True:
    
    try:
        for stock in stockList:
            os.system('cls')
            stockCode = stock['code'] + '.NS'
            news = yf.Ticker(stockCode).get_news()

            if len(news) == 0:
                updates = {
                    "prediction" : get_prediction(stockCode, 0),
                    "latest_headline": "",
                    "latest_article": "",
                    "impact_score": 0,
                    "updated_at": datetime.datetime.utcnow()
                }

                result = collection.update_one(
                    {"code": stockCode.replace('.NS', '')},
                    {"$set": updates}
                )

                continue

        
            for article in news:
                content = article['content']['summary']
                title = article['content']['title']
            
                response = json.loads(Evaluate(content))['impact']

                impact_score = float(response)

                updates = {
                    "prediction" : get_prediction(stockCode, impact_score),
                    "latest_headline": title,
                    "latest_article": content,
                    "impact_score": impact_score,
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