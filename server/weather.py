from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool(name="get_weather", description="Get the weather for a given city")
async def get_weather(city: str) -> str:
    """get the weather for a given city"""
    return f"The weather in {city} is sunny"


@mcp.tool(name="get_temperature", description="Get the temperature for a given city")
async def get_temperature(city: str) -> str:
    """get the temperature for a given city"""
    return f"The temperature in {city} is 25 degrees Celsius"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    
