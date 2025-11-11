from google.adk.agents import SequentialAgent, LoopAgent
from .sub_agent.post_generate.agent import initial_post_generator
from .sub_agent.post_reviewer.agent import post_reviewer
from .sub_agent.post_refiner.agent import post_refiner

refinement_loop = LoopAgent(
    name="post_refinement_loop",
    max_iterations=10,
    sub_agents=[
        post_reviewer,
        post_refiner
    ],
    description="Iterate over Initial linkedin post with reviewer and refiner"
)

root_agent = SequentialAgent(
    name="linkedin_post_agent",
    sub_agents=[initial_post_generator, refinement_loop]
)