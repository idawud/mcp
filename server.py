from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import inspect

# Import all products
from products.etf_product import ETFProduct
from products.future_product import FutureProduct
from products.option_product import OptionProduct
from products.stock_product import StockProduct
from products.fx_product import FXProduct

mcp = FastMCP("FinanceService")

# Initialize all products
products = [
    ETFProduct(),
    FutureProduct(),
    OptionProduct(),
    StockProduct(),
    FXProduct(),
]

# Helper function to convert data to serializable format
def to_dict(obj: Any) -> Any:
    """Convert objects to dictionaries for JSON serialization"""
    if hasattr(obj, '__dataclass_fields__'):
        return vars(obj)
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    else:
        return obj

# Dynamically register all tools from all products
for product in products:
    product_name = product.name.lower()
    
    for tool_name, method, description in product.get_tools():
        # Get method signature for tool definition
        sig = inspect.signature(method)
        
        # Create wrapper function that converts results to dicts
        def create_tool_wrapper(m, p_name):
            def tool_wrapper(*args, **kwargs):
                result = m(*args, **kwargs)
                return to_dict(result)
            return tool_wrapper
        
        # Build tool name with product prefix
        full_tool_name = f"{product_name}_{tool_name}"
        
        # Register the tool with MCP
        mcp.tool(name=full_tool_name, description=description)(
            create_tool_wrapper(method, product_name)
        )

if __name__ == "__main__":
    mcp.run()
