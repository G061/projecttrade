"""
News Sentiment Analysis using FinBERT or open-source transformer
"""
from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, model_name="ProsusAI/finbert"):
        self.nlp = pipeline("sentiment-analysis", model=model_name)

    def analyze(self, texts):
        """Analyze sentiment of a list of texts (news headlines, etc.)"""
        return self.nlp(texts)
