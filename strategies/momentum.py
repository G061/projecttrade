"""
Example Momentum Strategy Module
"""
from .base import StrategyBase
import pandas as pd

class MomentumStrategy(StrategyBase):
    def generate_signals(self, market_data):
        # Momentum with exits:
        # BUY when close > close.shift(5), SELL when close < close.shift(5), else HOLD
        df = pd.DataFrame(market_data).copy()
        df['close_shift_5'] = df['close'].shift(5)
        conditions = []
        for i in range(len(df)):
            if pd.isna(df['close_shift_5'].iloc[i]):
                conditions.append('HOLD')
            else:
                if df['close'].iloc[i] > df['close_shift_5'].iloc[i]:
                    conditions.append('BUY')
                elif df['close'].iloc[i] < df['close_shift_5'].iloc[i]:
                    conditions.append('SELL')
                else:
                    conditions.append('HOLD')
        df['signal'] = conditions
        return df['signal']

    def on_trade(self, trade_data):
        # Log or react to trade events
        pass
