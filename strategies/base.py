"""
Base Strategy class for plug-and-play modular strategies.
"""
from abc import ABC, abstractmethod

class StrategyBase(ABC):
    """Abstract base for all trading strategies."""
    def __init__(self, config=None):
        self.config = config or {}

    @abstractmethod
    def generate_signals(self, market_data):
        """Generate trading signals based on market data."""
        pass

    @abstractmethod
    def on_trade(self, trade_data):
        """React to trade events (fills, errors, etc.)."""
        pass

    @property
    def name(self):
        return self.__class__.__name__
