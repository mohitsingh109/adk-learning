from google.adk.agents import SequentialAgent
from .sub_agent.validator.agent import lead_validator
from .sub_agent.scorer.agent import lead_score_agent
from .sub_agent.recommender.agent import lead_recommender_agent

root_agent = SequentialAgent(
    name="LeadQualificationAgent",
    sub_agents=[lead_validator, lead_score_agent, lead_recommender_agent],
    description="A pipeline that validate for sales lead"
)