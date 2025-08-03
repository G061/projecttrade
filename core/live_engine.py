"""
Live Trading Engine: Angel One SmartAPI, paper/live mode, risk management
"""
import os
from core.broker import get_broker

class LiveEngine:
    def __init__(self, broker_name="angelone", paper_mode=True, risk_config=None):
        self.broker = get_broker(broker_name)
        self.paper_mode = paper_mode
        self.risk_config = risk_config or {
            'max_capital_per_trade': 0.1,  # 10% of capital
            'max_daily_loss': 0.05,        # 5% of capital
            'stop_loss_pct': 0.02,         # 2% stop loss
            'target_pct': 0.04,            # 4% target
            'trailing_stop_pct': 0.01      # 1% trailing stop
        }
        self.daily_loss = 0
        self.capital = float(os.getenv('INITIAL_CAPITAL', 100000))
        self.positions = []
        self.trades = []
        self.circuit_breaker = False

    def authenticate(self):
        return self.broker.authenticate()

    def place_order(self, symbol, qty, side, order_type, price=None, sl=None, target=None, **kwargs):
        if self.circuit_breaker:
            print("Trading halted: circuit breaker triggered.")
            return None
        if self.paper_mode:
            # Simulate order
            trade = {'symbol': symbol, 'qty': qty, 'side': side, 'order_type': order_type, 'price': price, 'paper': True}
            self.trades.append(trade)
            return trade
        else:
            # Live order
            response = self.broker.place_order(symbol, qty, side, order_type, price, sl, target, **kwargs)
            self.trades.append(response)
            return response

    def check_risk(self, trade_pnl):
        self.daily_loss += trade_pnl if trade_pnl < 0 else 0
        if abs(self.daily_loss) > self.risk_config['max_daily_loss'] * self.capital:
            self.circuit_breaker = True
            print("Max daily loss hit: circuit breaker activated.")

    def reset_daily(self):
        self.daily_loss = 0
        self.circuit_breaker = False
        self.trades = []
