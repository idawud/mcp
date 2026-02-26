import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclasses import dataclass
from typing import Optional, List, Any
from utils.load_utils import load_json_data
from products.base_product import BaseProduct

@dataclass
class StockSchema:
    '''
    Docstring for StockSchema
    '''
    id: Optional[Any] = None
    symbol: Optional[Any] = None
    name: Optional[Any] = None
    exchange: Optional[Any] = None
    sector: Optional[Any] = None
    market_cap: Optional[Any] = None
    current_price: Optional[Any] = None
    volume: Optional[Any] = None
    pe_ratio: Optional[Any] = None
    dividend_yield: Optional[Any] = None
    week_52_high: Optional[Any] = None
    week_52_low: Optional[Any] = None
    currency: Optional[Any] = None

    @staticmethod
    def from_dict(data: dict):
        return StockSchema(
            id=data.get("id", None),
            symbol=data.get("symbol", None),
            name=data.get("name", None),
            exchange=data.get("exchange", None),
            sector=data.get("sector", None),
            market_cap=data.get("market_cap", None),
            current_price=data.get("current_price", None),
            volume=data.get("volume", None),
            pe_ratio=data.get("pe_ratio", None),
            dividend_yield=data.get("dividend_yield", None),
            week_52_high=data.get("week_52_high", None),
            week_52_low=data.get("week_52_low", None),
            currency=data.get("currency", None),
        )

    @staticmethod
    def bulk(data: list):
        return [StockSchema.from_dict(item) for item in data]

class StockProduct(BaseProduct):
    def __init__(self):
        super().__init__("Stock")
        self.data: List[StockSchema] = load_json_data("stock.json", lambda_func=lambda d: StockSchema.bulk(d.get('stocks', [])))
        print(f"Loaded {len(self.data)} Stock products from ./data/stock.json")
        
        # Register tools
        self.register_tool("get_all", self.get_all_data, "Get all Stock products")
        self.register_tool("get_by_symbol", self.get_data_by_symbol, "Get stock by symbol")
        self.register_tool("get_by_sector", self.get_data_by_sector, "Get stocks by sector")
        self.register_tool("get_by_exchange", self.get_data_by_exchange, "Get stocks by exchange")
        self.register_tool("get_52_week_range", self.calculate_52_week_range, "Get 52-week range")
        self.register_tool("get_highest_market_cap", self.get_highest_market_cap, "Get stock with highest market cap")
        self.register_tool("get_highest_dividend", self.get_highest_dividend_yield, "Get stock with highest dividend yield")
    
    def get_schema(self) -> set:
        return set(StockSchema.__annotations__.keys())
    
    def get_all_data(self) -> List[StockSchema]:
        return self.data
    
    def get_data_by_symbol(self, symbol: str) -> Optional[StockSchema]:
        for item in self.data:
            if item.symbol == symbol:
                return item
        return None
    
    def get_data_by_sector(self, sector: str) -> List[StockSchema]:
        return [item for item in self.data if item.sector == sector]
    
    def get_data_by_exchange(self, exchange: str) -> List[StockSchema]:
        return [item for item in self.data if item.exchange == exchange]
    
    def calculate_52_week_range(self, symbol: str) -> Optional[dict]:
        stock = self.get_data_by_symbol(symbol)
        if stock and stock.week_52_high and stock.week_52_low:
            return {
                "high": stock.week_52_high,
                "low": stock.week_52_low,
                "range": stock.week_52_high - stock.week_52_low
            }
        return None
    
    def get_highest_market_cap(self) -> Optional[StockSchema]:
        return max(self.data, key=lambda x: x.market_cap if x.market_cap else 0) if self.data else None
    
    def get_highest_dividend_yield(self) -> Optional[StockSchema]:
        return max(self.data, key=lambda x: x.dividend_yield if x.dividend_yield else 0) if self.data else None
