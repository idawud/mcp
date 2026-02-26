import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclasses import dataclass
from typing import Optional, List, Any
from utils.load_utils import load_json_data
from products.base_product import BaseProduct

@dataclass
class OptionSchema:
    '''
    Docstring for OptionSchema
    '''
    id: Optional[Any] = None
    underlying_symbol: Optional[Any] = None
    underlying_price: Optional[Any] = None
    option_type: Optional[Any] = None
    strike: Optional[Any] = None
    expiration_date: Optional[Any] = None
    days_to_expiry: Optional[Any] = None
    bid: Optional[Any] = None
    ask: Optional[Any] = None
    last_price: Optional[Any] = None
    volume: Optional[Any] = None
    open_interest: Optional[Any] = None
    implied_volatility: Optional[Any] = None
    delta: Optional[Any] = None
    gamma: Optional[Any] = None
    theta: Optional[Any] = None
    vega: Optional[Any] = None
    currency: Optional[Any] = None

    @staticmethod
    def from_dict(data: dict):
        return OptionSchema(
            id=data.get("id", None),
            underlying_symbol=data.get("underlying_symbol", None),
            underlying_price=data.get("underlying_price", None),
            option_type=data.get("option_type", None),
            strike=data.get("strike", None),
            expiration_date=data.get("expiration_date", None),
            days_to_expiry=data.get("days_to_expiry", None),
            bid=data.get("bid", None),
            ask=data.get("ask", None),
            last_price=data.get("last_price", None),
            volume=data.get("volume", None),
            open_interest=data.get("open_interest", None),
            implied_volatility=data.get("implied_volatility", None),
            delta=data.get("delta", None),
            gamma=data.get("gamma", None),
            theta=data.get("theta", None),
            vega=data.get("vega", None),
            currency=data.get("currency", None),
        )

    @staticmethod
    def bulk(data: list):
        return [OptionSchema.from_dict(item) for item in data]

class OptionProduct(BaseProduct):
    def __init__(self):
        super().__init__("Option")
        self.data: List[OptionSchema] = load_json_data("option.json", lambda_func=lambda d: OptionSchema.bulk(d.get('options', [])))
        print(f"Loaded {len(self.data)} Option products from ./data/option.json")
        
        # Register tools
        self.register_tool("get_all", self.get_all_data, "Get all Option products")
        self.register_tool("get_by_underlying", self.get_data_by_underlying, "Get options by underlying symbol")
        self.register_tool("get_calls", self.get_calls, "Get call options for underlying")
        self.register_tool("get_puts", self.get_puts, "Get put options for underlying")
        self.register_tool("get_by_strike", self.get_data_by_strike, "Get options by strike price")
        self.register_tool("calculate_spread", self.calculate_bid_ask_spread, "Calculate bid-ask spread")
        self.register_tool("get_highest_iv", self.get_highest_implied_volatility, "Get option with highest IV")
    
    def get_schema(self) -> set:
        return set(OptionSchema.__annotations__.keys())
    
    def get_all_data(self) -> List[OptionSchema]:
        return self.data
    
    def get_data_by_underlying(self, underlying_symbol: str) -> List[OptionSchema]:
        return [item for item in self.data if item.underlying_symbol == underlying_symbol]
    
    def get_calls(self, underlying_symbol: str) -> List[OptionSchema]:
        return [item for item in self.data if item.underlying_symbol == underlying_symbol and item.option_type == "call"]
    
    def get_puts(self, underlying_symbol: str) -> List[OptionSchema]:
        return [item for item in self.data if item.underlying_symbol == underlying_symbol and item.option_type == "put"]
    
    def get_data_by_strike(self, strike: float) -> List[OptionSchema]:
        return [item for item in self.data if item.strike == strike]
    
    def calculate_bid_ask_spread(self, option_id: str) -> Optional[float]:
        option = next((item for item in self.data if item.id == option_id), None)
        if option and option.bid and option.ask:
            return option.ask - option.bid
        return None
    
    def get_highest_implied_volatility(self) -> Optional[OptionSchema]:
        return max(self.data, key=lambda x: x.implied_volatility if x.implied_volatility else 0) if self.data else None
