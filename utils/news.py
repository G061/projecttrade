"""
News Scraper for Economic Times, Moneycontrol
"""
import requests
from bs4 import BeautifulSoup

def scrape_economic_times_headlines():
    url = "https://economictimes.indiatimes.com/markets/stocks/news"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = [h.text.strip() for h in soup.select(".eachStory h3")]
    return headlines

def scrape_moneycontrol_headlines():
    url = "https://www.moneycontrol.com/news/business/markets/"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = [h.text.strip() for h in soup.select(".clearfix .article_title")]
    return headlines
