from google.adk.agents import Agent

question_answering_agent = Agent(
    name="question_answering_agent",
    model="gemini-2.0-flash",
    description="Question answering agent",
    instruction="""
    You are helpful Q/A assistant
    
    Here is some information about user:
    Name:
    {user_name}
    Preference:
    {user_preference}
    """
)