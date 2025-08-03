"""
Candlestick Pattern Recognition Utility
"""
import pandas as pd

def is_bullish_engulfing(df):
    return (df['close'] > df['open']) & (df['open'].shift(1) > df['close'].shift(1)) & (df['close'] > df['open'].shift(1)) & (df['open'] < df['close'].shift(1))

def is_bearish_engulfing(df):
    return (df['close'] < df['open']) & (df['open'].shift(1) < df['close'].shift(1)) & (df['close'] < df['open'].shift(1)) & (df['open'] > df['close'].shift(1))
