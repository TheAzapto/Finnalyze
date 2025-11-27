import requests
from bs4 import BeautifulSoup
import json
from time import sleep

url = "https://www.livemint.com/market/stock-market-news"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def scrape_latest_article_link(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        headlines = []
        
        news_list = soup.find('div', id="listview")

        if news_list:
            headline = news_list.find_all('h2', class_="headline")
            for h in headline:
                headlines.append(h.find('a').get('href'))


    
    except Exception as e:
        print(f"Error: {e}")
    
    return headlines[2]

def scrape_article(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        article_list = []
        article_div = soup.find_all('div', class_="storyParagraph")
        
        for index in article_div:
            article_list.append(index.get_text(strip=True))

        article = "".join(article_list[:-2])
    except Exception as e:
        print(f"Error: {e}")
    
    return article

if __name__ == "__main__":

    article_link = scrape_latest_article_link(url, headers)
    article = scrape_article("https://www.livemint.com" + article_link, headers)

    response = requests.post(
    'http://localhost:5000/analyze',
    json={"article": article}
    )

    for i in response.json():
        print(i)
