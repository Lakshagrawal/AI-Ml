from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
import logging

# Set up logging to see agent thinking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Optional: Enable LangSmith tracing (uncomment if you have LangSmith set up)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"

async def main():
    # Set environment variables first
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
    print("*"*100)
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["../server/mathserver.py"],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )
    print("*"*100)
    tools = await client.get_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    print("*"*100)
    modelAnthropic = ChatAnthropic(model="claude-3-7-sonnet-20250219", api_key=os.getenv("ANTHROPIC_API_KEY"), temperature=0.5)

    # model = ChatGroq(model="qwen-qwq-32b")
    print("*"*100)
    agent = create_react_agent(modelAnthropic, tools, checkpointer=None, interrupt_before=[], interrupt_after=[], debug=True)
    print("*"*100)

    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in jaipur?"}]})
    print("*"*100)
    print("🤖 Agent Response:")
    print(weather_response)
    print("*"*100)

    math_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what is 10*(8/4) + 20?"}]})
    print("*"*100)
    print("🤖 Agent Response:")
    print(math_response)
    print("*"*100)


asyncio.run(main())
