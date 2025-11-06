import uuid
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from question_answering_agent.agent import question_answering_agent

load_dotenv()

session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Mohit Singh",
    "user_preference": """
        I like to play basketball
        My loveable dish is pizza
    """
}

SESSION_ID = str(uuid.uuid4())
APP_NAME = "Q/A Bot"
USER_ID = "mohit_109"
stateful_session: Session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

print("SESSION CREATED")
print("SESSION_ID", SESSION_ID)

runner = Runner(
    agent=question_answering_agent,
    session_service=stateful_session,
    app_name=APP_NAME
)

# for event in runner.run(
#     user_id=USER_ID,
#     session_id=SESSION_ID,
#     new_message=new_message
# ):
#     if event.is_final_response():
#         if event.content:
#             print("Final response: ", event.content.parts[0].text)