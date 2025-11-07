from google.adk.agents import Agent
from google.adk.tools import ToolContext


def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    jokes = {
        "python": "Why was the Python developer always borrowing money? Because they kept running out of 'C'!",
        "javascript": "Why did the JavaScript developer wear glasses? Because they couldn't C#!",
        "html": "Why was the HTML tag sad? Because it couldn't find its 'style'!",
        "database": "Why did the developer quit their job? They didn't get arrays!",
        "default": "There are only 10 types of people in the world: those who understand binary, and those who don't."
    }
    joke = jokes.get(topic, jokes["default"])
    tool_context.state["last_jock_topic"] = topic
    return {
        "stats": "success",
        "joke": joke,
        "topic": topic
    }

"""
default response structure
{
    "result": "...."
}
"""

funny_nerd = Agent(
    name="funny_nerd",
    model="gemini-2.0-flash",
    description="An agent that tells nerdy jokes about various topic",
    instruction="""
    ### Tool Usage Guidelines: get_nerd_joke(topic)

    You have access to the `get_nerd_joke(topic)` tool. This tool retrieves a programming or tech-related joke based on the specified string argument, 'topic'.
    
    **Strict Rules for Tool Use:**
    
    1.  **Mandatory Use Cases (When to Call):**
        * When a user explicitly requests a joke and mentions a **technical concept, language, or field** (e.g., "Tell me a joke about Python," "Got any good JavaScript humor?").
        * When a user simply asks for a joke ("Tell me a joke"), you must call the tool with a relevant, recent, or default topic (e.g., call `get_nerd_joke("default")`).
    
    2.  **Argument Formulation:**
        * The 'topic' argument must be a **single, specific keyword** extracted from the user's request (e.g., "python", "javascript", "html", "database").
        * If the user's request is general, use `"default"` as the topic argument.
    
    3.  **Prohibited Use Cases (When NOT to Call):**
        * Do not call the tool if the user's request for humor is clearly **not** technical or programmer-related (e.g., "Tell me a knock-knock joke," "Tell me a cat joke").
        * Do not use the tool for non-humorous, factual questions.
    
    **Response Strategy:**
    * When the tool returns a joke, you must present the joke clearly and enthusiastically.
    
    **Goal:** Provide context-specific technical humor to the user by intelligently identifying and passing the relevant topic to the tool.
    
    If the user ask anything else,
    you should delegate the task to the manager agent
    """,
    tools=[get_nerd_joke]
)