import sys
from pathlib import Path
from abc import ABC
from typing import List, Tuple, Callable, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class BaseProduct(ABC):
    """Base class for all product types with tool registry"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: List[Tuple[str, Callable, str]] = []
    
    def register_tool(self, tool_name: str, method: Callable, description: str) -> None:
        """Register a tool method with MCP server"""
        self.tools.append((tool_name, method, description))
    
    def get_tools(self) -> List[Tuple[str, Callable, str]]:
        """Get all registered tools"""
        return self.tools
    
    def get_schema(self) -> set:
        """Get schema fields for this product"""
        raise NotImplementedError
    
    def get_all_data(self) -> List[Any]:
        """Get all data for this product"""
        raise NotImplementedError
