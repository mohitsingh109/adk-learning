from google.adk import Runner
from google.adk.events.event import Event
from google.genai import types

async def call_agent_async(runner: Runner, user_id: str, session_id: str, query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"--- Running Query: {query} ---")

    final_response_text = None
    agent_name = None

    # DEBUG: Display state before processing the message

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)

            if response:
                final_response_text = response

    except Exception as e:
        print(f"Error during agent run: {e}")

    # DEBUG: Display state after processing the message
    return final_response_text


async def process_agent_response(event: Event):
    print(f"Event Id: {event.id}, Author: {event.author}")

    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f" Text: '{part.text}'")

    final_response = None

    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text") # text key (text: None)
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text
            print(f"----Agent Response---- {final_response}")

    return final_response