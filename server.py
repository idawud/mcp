from mcp.server.fastmcp import FastMCP

# Initialize FastMCP - the easiest way to build
mcp = FastMCP("WeatherService")

@mcp.tool()
def get_weather(city: str) -> str:
    """Provides the current weather for a given city."""
    # In a real app, you'd call an actual API here
    if city.lower() == "london":
        return "It's 15°C and cloudy."
    return f"The weather in {city} is sunny and 22°C."

if __name__ == "__main__":
    mcp.run()