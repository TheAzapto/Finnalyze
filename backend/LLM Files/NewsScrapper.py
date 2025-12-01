import json
import yfinance as yf
import datetime
from pymongo import MongoClient
from FinLlama_Middleware import Evaluate
from time import sleep
import os
from predictor import get_prediction

client = MongoClient('mongodb+srv://root:1234@cluster0.260lmcy.mongodb.net/')
db = client['Finnalyze']
collection = db['stockData']


with open('backend\stockList.json', 'r') as f:
    stockList = json.load(f)

epoch = 0
update_count = 0

while True:
    
    try:
        for stock in stockList:
            os.system('cls')
            # print(f"Epoch {epoch}")
            # print(f"Updated {update_count} stocks")
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

                update_count += 1

                continue

        
            for article in news:
                content = article['content']['summary']
                title = article['content']['title']
            
                response = Evaluate(content)

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

                update_count += 1
                
                

        sleep(600)
        epoch += 1
                
    except KeyboardInterrupt as e:
        break

    except Exception as e:
        print(e)
        continue