"""
Example Momentum Strategy Module
"""
from .base import StrategyBase
import pandas as pd

class MomentumStrategy(StrategyBase):
    def generate_signals(self, market_data):
        # Simple momentum: buy if close > close.shift(5)
        df = pd.DataFrame(market_data)
        signal = []
        for i in range(len(df)):
            if i >= 5 and df['close'].iloc[i] > df['close'].iloc[i-5]:
                signal.append('BUY')
            else:
                signal.append('HOLD')
        df['signal'] = signal
        return df['signal']

    def on_trade(self, trade_data):
        # Log or react to trade events
        pass
