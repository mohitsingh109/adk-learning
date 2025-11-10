from google.adk.agents import Agent
from .tools import refund_course


policy_agent = Agent(
    name="order_agent",
    model="gemini-2.0-flash",
    description="Agent dedicated to refunding the purchased course",
    instruction=""" """,
    tools=[refund_course]
)