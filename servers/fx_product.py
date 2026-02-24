
from dataclasses import dataclass, field
from typing import Optional, List, Any

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

class FXProduct:
    def __init__(self):
        # load product details from a json file ./data/fx.json of schema FXSchema
        import json 
        with open("./data/fx.json", "r") as f:
            raw = json.load(f)
            self.data = FXSchema.bulk(raw.get('fx', []))
        print(f"Loaded {len(self.data)} FX products from ./data/fx.json")
    
    def get_schema(self) -> set:
        return set(FXSchema.__annotations__.keys())
    