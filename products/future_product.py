import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclasses import dataclass
from typing import Optional, List, Any
from utils.load_utils import load_json_data
from products.base_product import BaseProduct

@dataclass
class FutureSchema:
    '''
    Docstring for FutureSchema
    '''
    id: Optional[Any] = None
    symbol: Optional[Any] = None
    name: Optional[Any] = None
    exchange: Optional[Any] = None
    contract_size: Optional[Any] = None
    tick_size: Optional[Any] = None
    tick_value: Optional[Any] = None
    months: Optional[Any] = None
    current_price: Optional[Any] = None
    volume: Optional[Any] = None
    open_interest: Optional[Any] = None
    currency: Optional[Any] = None
    last_trading_day: Optional[Any] = None

    @staticmethod
    def from_dict(data: dict):
        return FutureSchema(
            id=data.get("id", None),
            symbol=data.get("symbol", None),
            name=data.get("name", None),
            exchange=data.get("exchange", None),
            contract_size=data.get("contract_size", None),
            tick_size=data.get("tick_size", None),
            tick_value=data.get("tick_value", None),
            months=data.get("months", None),
            current_price=data.get("current_price", None),
            volume=data.get("volume", None),
            open_interest=data.get("open_interest", None),
            currency=data.get("currency", None),
            last_trading_day=data.get("last_trading_day", None),
        )

    @staticmethod
    def bulk(data: list):
        return [FutureSchema.from_dict(item) for item in data]

class FutureProduct(BaseProduct):
    def __init__(self):
        super().__init__("Future")
        self.data: List[FutureSchema] = load_json_data("future.json", lambda_func=lambda d: FutureSchema.bulk(d.get('futures', [])))
        print(f"Loaded {len(self.data)} Future products from ./data/future.json")
        
        # Register tools
        self.register_tool("get_all", self.get_all_data, "Get all Future products")
        self.register_tool("get_by_symbol", self.get_data_by_symbol, "Get Future by symbol")
        self.register_tool("get_by_exchange", self.get_data_by_exchange, "Get futures by exchange")
        self.register_tool("calculate_contract_value", self.calculate_contract_value, "Calculate contract value")
        self.register_tool("get_highest_volume", self.get_highest_volume, "Get future with highest volume")
    
    def get_schema(self) -> set:
        return set(FutureSchema.__annotations__.keys())
    
    def get_all_data(self) -> List[FutureSchema]:
        return self.data
    
    def get_data_by_symbol(self, symbol: str) -> Optional[FutureSchema]:
        for item in self.data:
            if item.symbol == symbol:
                return item
        return None
    
    def get_data_by_exchange(self, exchange: str) -> List[FutureSchema]:
        return [item for item in self.data if item.exchange == exchange]
    
    def calculate_contract_value(self, symbol: str) -> Optional[float]:
        future = self.get_data_by_symbol(symbol)
        if future and future.current_price and future.contract_size:
            return future.current_price * future.contract_size
        return None
    
    def get_highest_volume(self) -> Optional[FutureSchema]:
        return max(self.data, key=lambda x: x.volume if x.volume else 0) if self.data else None
