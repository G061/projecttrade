"""
Risk Management Engine: stop loss, target, trailing stop, max capital/trade, max daily loss, circuit breaker
"""
import os
import json

class RiskEngine:
    def __init__(self, config=None):
        self.config = config or {
            'stop_loss_pct': 0.02,
            'target_pct': 0.04,
            'trailing_stop_pct': 0.01,
            'max_capital_per_trade': 0.1,
            'max_daily_loss': 0.05,
        }
        self.daily_loss = 0
        self.circuit_breaker = False

    def check_trade(self, capital, trade_size, trade_loss):
        if trade_size > self.config['max_capital_per_trade'] * capital:
            return False, "Trade size exceeds max capital per trade."
        if self.circuit_breaker:
            return False, "Circuit breaker active."
        return True, "OK"

    def update_daily_loss(self, loss, capital):
        self.daily_loss += loss
        if abs(self.daily_loss) > self.config['max_daily_loss'] * capital:
            self.circuit_breaker = True
            return False, "Max daily loss hit. Circuit breaker activated."
        return True, "OK"

    def reset_daily(self):
        self.daily_loss = 0
        self.circuit_breaker = False

    # --- Persistence helpers ---
    def save_state(self, path=os.path.join('logs', 'risk_state.json')):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        state = {
            'daily_loss': self.daily_loss,
            'circuit_breaker': self.circuit_breaker,
            'config': self.config,
        }
        with open(path, 'w') as f:
            json.dump(state, f)

    def load_state(self, path=os.path.join('logs', 'risk_state.json')):
        if not os.path.exists(path):
            return False
        try:
            with open(path) as f:
                state = json.load(f)
            self.daily_loss = state.get('daily_loss', 0)
            self.circuit_breaker = state.get('circuit_breaker', False)
            # keep current config if present; ignore persisted config differences
            return True
        except Exception:
            return False
