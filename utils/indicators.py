"""
Technical Indicators Utility Module
"""
import pandas as pd

def sma(series, period):
    return series.rolling(window=period).mean()

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    # Prevent divide-by-zero; add small epsilon to denominator
    eps = 1e-10
    denom = loss.where(loss > 0, eps)
    rs = gain / denom
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)
