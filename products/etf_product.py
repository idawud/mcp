import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclasses import dataclass
from typing import Optional, List, Any
from utils.load_utils import load_json_data
from products.base_product import BaseProduct

@dataclass
class ETFSchema:
    '''
    Docstring for ETFSchema
    '''
    id: Optional[Any] = None
    symbol: Optional[Any] = None
    name: Optional[Any] = None
    asset_class: Optional[Any] = None
    expense_ratio: Optional[Any] = None
    nav: Optional[Any] = None
    volume: Optional[Any] = None
    dividend_yield: Optional[Any] = None
    inception_date: Optional[Any] = None
    aum: Optional[Any] = None
    holdings_count: Optional[Any] = None
    currency: Optional[Any] = None

    @staticmethod
    def from_dict(data: dict):
        return ETFSchema(
            id=data.get("id", None),
            symbol=data.get("symbol", None),
            name=data.get("name", None),
            asset_class=data.get("asset_class", None),
            expense_ratio=data.get("expense_ratio", None),
            nav=data.get("nav", None),
            volume=data.get("volume", None),
            dividend_yield=data.get("dividend_yield", None),
            inception_date=data.get("inception_date", None),
            aum=data.get("aum", None),
            holdings_count=data.get("holdings_count", None),
            currency=data.get("currency", None),
        )

    @staticmethod
    def bulk(data: list):
        return [ETFSchema.from_dict(item) for item in data]

class ETFProduct(BaseProduct):
    def __init__(self):
        super().__init__("ETF")
        self.data: List[ETFSchema] = load_json_data("etf.json", lambda_func=lambda d: ETFSchema.bulk(d.get('etfs', [])))
        print(f"Loaded {len(self.data)} ETF products from ./data/etf.json")
        
        # Register tools
        self.register_tool("get_all", self.get_all_data, "Get all ETF products")
        self.register_tool("get_by_symbol", self.get_data_by_symbol, "Get ETF by symbol")
        self.register_tool("get_by_asset_class", self.get_data_by_asset_class, "Get ETFs by asset class")
        self.register_tool("get_lowest_expense", self.get_lowest_expense_ratio, "Get ETF with lowest expense ratio")
        self.register_tool("get_highest_aum", self.get_highest_aum, "Get ETF with highest AUM")
    
    def get_schema(self) -> set:
        return set(ETFSchema.__annotations__.keys())
    
    def get_all_data(self) -> List[ETFSchema]:
        return self.data
    
    def get_data_by_symbol(self, symbol: str) -> Optional[ETFSchema]:
        for item in self.data:
            if item.symbol == symbol:
                return item
        return None
    
    def get_data_by_asset_class(self, asset_class: str) -> List[ETFSchema]:
        return [item for item in self.data if item.asset_class == asset_class]
    
    def get_lowest_expense_ratio(self) -> Optional[ETFSchema]:
        return min(self.data, key=lambda x: x.expense_ratio if x.expense_ratio else float('inf')) if self.data else None
    
    def get_highest_aum(self) -> Optional[ETFSchema]:
        return max(self.data, key=lambda x: x.aum if x.aum else 0) if self.data else None
