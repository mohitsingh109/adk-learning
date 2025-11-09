"""
Entry point of our application
mostly it will have some POST, GET http endpoints
"""
import asyncio

from customer_service_agent.agent import customer_service_agent
from utils import call_agent_async
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv

load_dotenv()
session_service = InMemorySessionService()

initial_state = {
    "user_name": "Mohit Singh",
    "purchased_courses": [],
    "intersection_history": []
}

async def main_async():
    APP_NAME = "Customer Support"
    USER_ID = "mohitsingh109" # this will be the client id

    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )

    SESSION_ID = new_session.id
    print(f"Created Session: {SESSION_ID}")

    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("Welcome to Customer Service chat")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation...")
            break

        # we'll call the runner by passing the user_input
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


def main():
    """Entry point for the application"""
    asyncio.run(main_async())


if __name__ == '__main__':
    main()