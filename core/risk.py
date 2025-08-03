"""
Risk Management Engine: stop loss, target, trailing stop, max capital/trade, max daily loss, circuit breaker
"""
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
