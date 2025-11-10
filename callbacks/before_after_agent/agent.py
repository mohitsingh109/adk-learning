from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types


def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    # Optional[types.Content]: we'll return this if we want to reject the agent processing
    """
    Return:
         None to continue the normal agent processing
    """
    state = callback_context.state

    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatBot"

    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1

    timestamp = datetime.now()
    state["request_state_time"] = timestamp

    print("AGENT EXECUTION STARTED")
    print(f"Request #: {state["request_counter"]}")
    print(f"Timestamp: {timestamp}")

    return None

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
        Return:
             None to continue the normal agent processing
    """
    state = callback_context.state
    timestamp = datetime.now()
    duration = None
    if "request_state_time" in state:
        duration = (timestamp - state["request_state_time"]).total_seconds()

    print("=== Agent execution completed ===")
    print(f"Request #: {state["request_counter"]}")
    print(f"Duration #: {duration}")

    return None

root_agent = LlmAgent(
    name="before_after_agent", # it will be a dashboard agent
    model="gemini-2.0-flash",
    description="A basic agent to learn before after callback",
    before_agent_callback=before_agent_callback, # here I'll check if user has access for dashboard agent to run
    instruction="""
        You are a greeting agent. your name is {agent_name}.
        
        Your Job is to greet user with politely & friendly way
    """,
    after_agent_callback=after_agent_callback
)