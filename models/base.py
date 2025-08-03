"""
Base class for AI/ML models (LSTM, Transformer, etc.)
"""
from abc import ABC, abstractmethod

class ModelBase(ABC):
    def __init__(self, config=None):
        self.config = config or {}

    @abstractmethod
    def train(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    @property
    def name(self):
        return self.__class__.__name__
