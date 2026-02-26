
import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclasses import dataclass, field
from typing import Optional, List, Any
from utils.load_utils import load_json_data
from products.base_product import BaseProduct

@dataclass
class FXSchema:
    '''
    Docstring for FXSchema
    '''
    id: Optional[Any] = None
    pair: Optional[Any] = None
    base_currency: Optional[Any] = None
    quote_currency: Optional[Any] = None
    bid: Optional[Any] = None
    ask: Optional[Any] = None
    mid: Optional[Any] = None
    spread_pips: Optional[Any] = None
    daily_change: Optional[Any] = None
    daily_change_percent: Optional[Any] = None
    daily_high: Optional[Any] = None
    daily_low: Optional[Any] = None
    weekly_high: Optional[Any] = None
    weekly_low: Optional[Any] = None
    monthly_high: Optional[Any] = None
    monthly_low: Optional[Any] = None
    volume_24h: Optional[Any] = None
    major_support: Optional[Any] = None
    major_resistance: Optional[Any] = None
    pip_value: Optional[Any] = None
    swap_long: Optional[Any] = None
    swap_short: Optional[Any] = None
    trading_hours: Optional[Any] = None
    market_sentiment: Optional[Any] = None
    volatility_24h: Optional[Any] = None
    correlation_oil: Optional[Any] = None
    correlation_rbi_intervention: Optional[Any] = None
    central_bank_rate: Optional[Any] = None
    next_economic_release: Optional[Any] = None

    @staticmethod
    def from_dict(data: dict):
        return FXSchema(
            id=data.get("id", None),
            pair=data.get("pair", None),
            base_currency=data.get("base_currency", None),
            quote_currency=data.get("quote_currency", None),
            bid=data.get("bid", None),
            ask=data.get("ask", None),
            mid=data.get("mid", None),
            spread_pips=data.get("spread_pips", None),
            daily_change=data.get("daily_change", None),
            daily_change_percent=data.get("daily_change_percent", None),
            daily_high=data.get("daily_high", None),
            daily_low=data.get("daily_low", None),
            weekly_high=data.get("weekly_high", None),
            weekly_low=data.get("weekly_low", None),
            monthly_high=data.get("monthly_high", None),
            monthly_low=data.get("monthly_low", None),
            volume_24h=data.get("volume_24h", None),
            major_support=data.get("major_support", None),
            major_resistance=data.get("major_resistance", None),
            pip_value=data.get("pip_value", None),
            swap_long=data.get("swap_long", None),
            swap_short=data.get("swap_short", None),
            trading_hours=data.get("trading_hours", None),
            market_sentiment=data.get("market_sentiment", None),
            volatility_24h=data.get("volatility_24h", None),
            correlation_oil=data.get("correlation_oil", None),
            correlation_rbi_intervention=data.get("correlation_rbi_intervention", None),
            central_bank_rate=data.get("central_bank_rate", None),
            next_economic_release=data.get("next_economic_release", None),
        )

    @staticmethod
    def bulk(data: list):
        return [FXSchema.from_dict(item) for item in data]

class FXProduct(BaseProduct):
    def __init__(self):
        super().__init__("FX")
        self.data: List[FXSchema] = load_json_data("fx.json", lambda_func=lambda d: FXSchema.bulk(d.get('fx', [])))
        print(f"Loaded {len(self.data)} FX products from ./data/fx.json")
        
        # Register tools
        self.register_tool("get_all", self.get_all_data, "Get all FX pairs")
        self.register_tool("get_by_pair", self.get_data_by_pair, "Get FX data by pair")
        self.register_tool("get_quote", self.get_quote, "Get FX quote for currency pair")
    
    def get_schema(self) -> set:
        return set(FXSchema.__annotations__.keys())
    
    def get_all_data(self) -> List[FXSchema]:
        return self.data
    
    def get_data_by_pair(self, pair: str) -> Optional[FXSchema]:
        for item in self.data:
            if item.pair == pair:
                return item
        return None
    
    def get_quote(self, base_ccy: str, over_ccy: str) -> dict:
        for item in self.data:
            if item.base_currency == base_ccy and item.quote_currency == over_ccy:
                return {
                    "base_currency": item.base_currency,
                    "quote_currency": item.quote_currency,
                    "bid": item.bid,
                    "ask": item.ask
                }
            elif item.base_currency == over_ccy and item.quote_currency == base_ccy:
                return {
                    "base_currency": over_ccy,
                    "quote_currency": base_ccy,
                    "bid": 1/item.ask if item.ask else None,
                    "ask": 1/item.bid if item.bid else None
                }
        return None