import uuid
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types
from question_answering_agent.agent import question_answering_agent

load_dotenv()


initial_state = {
    "user_name": "Mohit Singh",
    "user_preference": """
        I like to play basketball
        My loveable dish is pizza
        My favorite TV show is God of war
    """
}

SESSION_ID = str(uuid.uuid4())
APP_NAME = "Q/A Bot"
USER_ID = "mohit_109"
session_service_stateful = InMemorySessionService()

stateful_session = session_service_stateful.create_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

print("SESSION CREATED")
print("SESSION_ID", SESSION_ID)

runner = Runner(
    agent=question_answering_agent,
    session_service=session_service_stateful,
    app_name=APP_NAME
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What is mohit favorite TV show")]
)


for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print("Final response: ", event.content.parts[0].text)


# Fetch a session
session = session_service_stateful.get_session_sync(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)
print("user_id", session.user_id)
print("Print final Session state")
for key, value in session.state.items():
    print(f"{key} ==> {value}")

for event in session.events:
    print(f"{event}")

