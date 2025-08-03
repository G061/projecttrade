"""
Broker interface and Angel One SmartAPI integration for ProjectTrade.
Extensible to support 5paisa, Upstox, etc.
"""
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BrokerBase(ABC):
    """Abstract base class for all broker integrations."""
    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def place_order(self, symbol, qty, side, order_type, price=None, sl=None, target=None, **kwargs):
        pass

    @abstractmethod
    def get_positions(self):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @abstractmethod
    def cancel_order(self, order_id):
        pass

class AngelOneBroker(BrokerBase):
    def __init__(self):
        from smartapi import SmartConnect
        self.api_key = os.getenv("ANGEL_API_KEY")
        self.client_code = os.getenv("ANGEL_CLIENT_CODE")
        self.access_token = os.getenv("ANGEL_ACCESS_TOKEN")
        self.api = SmartConnect(api_key=self.api_key)
        self.session = None

    def authenticate(self):
        # Angel One: Use access token for session
        self.api.set_session(self.client_code, self.access_token)
        self.session = True
        return self.session

    def place_order(self, symbol, qty, side, order_type, price=None, sl=None, target=None, **kwargs):
        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": kwargs.get("symboltoken"),
            "transactiontype": side.upper(),
            "exchange": kwargs.get("exchange", "NSE"),
            "ordertype": order_type.upper(),
            "producttype": kwargs.get("producttype", "INTRADAY"),
            "duration": "DAY",
            "quantity": qty,
        }
        if price:
            order_params["price"] = price
        if sl:
            order_params["triggerprice"] = sl
        response = self.api.placeOrder(order_params)
        return response

    def get_positions(self):
        return self.api.position()

    def get_balance(self):
        return self.api.rmsLimit()

    def cancel_order(self, order_id):
        return self.api.cancelOrder(order_id)

# Factory for broker

def get_broker(name="angelone"):
    if name == "angelone":
        return AngelOneBroker()
    # Placeholder for future brokers
    raise NotImplementedError(f"Broker '{name}' not implemented yet.")
