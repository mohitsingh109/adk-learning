from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext, BaseTool
from google.genai import types
from typing import Dict, Any

def get_capital_city(country: str) -> Dict[str, str]:

    country_capital = {
        "india": "delhi",
        "usa": "abc",
        "canada": "xyz"
    }

    result = country_capital.get(country.lower(), f"Capital not found for {country}")
    print(f"[TOOL] Result {result}")
    return {
        "result": result
    }

def dummy(country: str) -> str:
    return "I am dummy"
"""
{
    "result": "I am dummy"
}
"""


def before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    tool_name = tool.name
    print(f"[Before TOOL CALLBACK] Started with name: {tool_name}, args: {args}")
    if tool_name == "get_capital_city" and args.get("country", "").lower() == "ind":
        print("[TOOL CALLBACK] Converting IND to india")
        args["country"] = "India"
        print(f"[TOOL CALLBACK Modified] args: {args}")

    print(f"[Before TOOL CALLBACK] Complete with name: {tool_name}, args: {args}")
    return None

def after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    tool_name = tool.name
    print(f"[AFTER TOOL CALLBACK] with name: {tool_name}, args: {args}, response: {tool_response}")
    return None

root_agent = LlmAgent(
    name="before_after_tool",  # it will be a dashboard agent
    model="gemini-2.0-flash",
    description="A basic agent to learn before after callback",
    instruction="""
        You are a geo agent.

        Your we'll provide the capital for a country
    """,
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
    tools=[get_capital_city]
)