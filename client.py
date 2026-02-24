import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 1. Point to your server script
    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"] 
    )

    # 2. Start the server and connect
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the protocol handshake
            await session.initialize()

            # 3. Discover what tools the server has
            tools = await session.list_tools()
            print(f"Server tools: {[t.name for t in tools.tools]}")

            # 4. Call the weather tool
            response = await session.call_tool("get_weather", arguments={"city": "London"})
            print(f"Tool Response: {response.content[0].text}")

if __name__ == "__main__":
    print("🚀 Starting MCP client...")
    asyncio.run(main())