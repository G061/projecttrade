"""
Modular Strategy Engine: dynamically loads and manages strategy modules.
"""
import importlib
import os
import glob
import inspect
from strategies.base import StrategyBase

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
            try:
                module = importlib.import_module(f"strategies.{name}")
            except Exception as e:
                print(f"[STRATEGY] Failed to import strategies.{name}: {e}")
                continue
            for attr in dir(module):
                obj = getattr(module, attr)
                if inspect.isclass(obj) and issubclass(obj, StrategyBase) and obj is not StrategyBase:
                    try:
                        self.strategies[name] = obj()
                    except Exception as e:
                        print(f"[STRATEGY] Failed to instantiate {attr} from {name}: {e}")

    def get_strategy(self, name):
        return self.strategies.get(name)

    def list_strategies(self):
        return list(self.strategies.keys())
