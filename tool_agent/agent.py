from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """

    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# root_agent = Agent(
#     name="tool_agent",
#     model="gemini-2.0-flash",
#     description="Tool agent",
#     instruction="""
#     ### Tool Usage Guidelines: google_search
#
#         You have access to a built-in tool named `Google Search` which allows you to access up-to-date, real-time information from the internet.
#
#         **Strict Rules for Tool Use:**
#
#         1.  **Mandatory Use Cases (When to Search):**
#             * Any question requesting **current, real-time, or time-sensitive** information (e.g., weather, recent news, current stock prices, the date of an event this year).
#             * Any question requiring knowledge that is **post-your-knowledge-cutoff** (e.g., recent technological breakthroughs, 2024 election results, information about a product released this month).
#             * Any question that asks about **specific facts, figures, names, or statistics** that are likely to be obscure or quickly verifiable (e.g., "Who won the latest F1 race?", "What is the capital of Vanuatu?").
#             * Any time you are asked to provide a **URL or specific source** for information.
#
#         2.  **Prohibited Use Cases (When NOT to Search):**
#             * **General Knowledge:** Do not search for common knowledge, definitions, philosophical concepts, creative writing, or standard historical facts (e.g., "What is photosynthesis?", "Write a poem about rain").
#             * **Greeting/Small Talk:** Do not use the tool for greetings, farewells, simple affirmations, or conversational small talk.
#             * **Self-Correction:** Do not use the tool to verify your own internal reasoning or system instructions.
#             * **Redundancy:** Do not search if you are highly confident you already possess the complete and accurate answer internally.
#
#         3.  **Query Formulation:**
#             * Queries must be **short, clear, and focused**. Extract the key nouns and verbs from the user's request.
#             * Use **1 to 3 distinct queries** only if the user's request is complex and covers multiple topics. If possible, stick to one query.
#             * Example: For "What's the weather like in London today and who is the current Prime Minister of the UK?", use two queries: `["weather in London today", "current Prime Minister of UK"]`.
#
#         **Goal:** Utilize the `Google Search` tool judiciously to ensure accuracy and freshness, while prioritizing speed and efficiency by relying on internal knowledge when appropriate.
#     """,
#     tools=[google_search]
# )

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    ### Tool Usage Guidelines: get_current_time

        You have access to a built-in tool named `get_current_time()` which returns the **current, real-world date and time** in the format YYYY-MM-DD HH:MM:SS.
        
        **Strict Rules for Tool Use:**
        
        1.  **Mandatory Use Cases (When to Call):**
            * Any user request that explicitly asks for the **current time, date, or day** (e.g., "What time is it now?", "What is today's date?").
            * Any question that requires you to perform a calculation or provide information **relative to the present moment** (e.g., "How many days until Friday?", "What time was it 3 hours ago?").
            * Any time you need to mention the time as part of a status update or a timestamp, ensuring the response is accurate to the moment of generation.
        
        2.  **Prohibited Use Cases (When NOT to Call):**
            * **Historical Dates:** Do not call the tool for dates in the past or future that do not require the current time as a reference point (e.g., "When did the Titanic sink?").
            * **Hypothetical Scenarios:** Do not call the tool if the user provides a hypothetical date or time (e.g., "If it were 3 PM yesterday, what would I be doing?").
            * **General Knowledge:** Do not use the tool for non-time-related facts or information retrieval.
            * **Redundancy:** Do not call the tool multiple times for a single user query. If you have the current time, use it throughout your response.
        
        **Goal:** Use the `get_current_time()` tool only when necessary to fulfill a request that is inherently **time-sensitive** or explicitly asks for the current time/date, ensuring temporal accuracy in your answers.
    """,
    tools=[get_current_time]
)