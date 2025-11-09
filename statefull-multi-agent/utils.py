from google.adk import Runner
from google.adk.events.event import Event
from google.genai import types

async def call_agent_async(runner: Runner, user_id: str, session_id: str, query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"--- Running Query: {query} ---")

    final_response_text = None
    agent_name = None

    # DEBUG: Display state before processing the message
    display_state(runner.session_service, runner.app_name, user_id, session_id,"State BEFORE processing")
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
    display_state(runner.session_service, runner.app_name, user_id, session_id, "State AFTER processing")
    return final_response_text


def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    print(f"==================Label: {label}==================")
    try:
        session = session_service.get_session_sync(
            app_name=app_name, user_id = user_id, session_id = session_id
        )

        user_name = session.state.get("user_name", "Unknown")
        print(f"👨🏼 User: {user_name}")

        purchased_courses = session.state.get("purchased_courses", [])

        if not purchased_courses:
            print(f"Course: None")

        for course in purchased_courses:
            id = course["id"]
            purchase_date = course["purchase_date"]
            print(f" - {id} (purchase on {purchase_date})")


    except Exception as e:
        print(f"Error displaying state {str(e)}")


async def process_agent_response(event: Event):
    print(f"Event Id: {event.id}, Author: {event.author}")

    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"\n Text: '{part.text}'\n")

    final_response = None

    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text") # text key (text: None)
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text
            print(f"\n----Agent Response----\n {final_response}")

    return final_response