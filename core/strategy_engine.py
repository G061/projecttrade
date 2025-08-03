"""
Modular Strategy Engine: dynamically loads and manages strategy modules.
"""
import importlib
import os
import glob

class StrategyEngine:
    def __init__(self, strategies_path="strategies"):
        self.strategies_path = strategies_path
        self.strategies = {}

    def discover_strategies(self):
        """Discover and load all strategy modules dynamically."""
        py_files = glob.glob(os.path.join(self.strategies_path, "*.py"))
        for file in py_files:
            name = os.path.basename(file)[:-3]
            if name.startswith("_") or name == "base":
                continue
            module = importlib.import_module(f"strategies.{name}")
            for attr in dir(module):
                obj = getattr(module, attr)
                if hasattr(obj, "__bases__") and "StrategyBase" in [b.__name__ for b in obj.__bases__]:
                    self.strategies[name] = obj()

    def get_strategy(self, name):
        return self.strategies.get(name)

    def list_strategies(self):
        return list(self.strategies.keys())
