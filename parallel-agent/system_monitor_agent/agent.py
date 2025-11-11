from google.adk.agents import ParallelAgent, SequentialAgent
from .sub_agent.cpu_info_agent.agent import cpu_info_agent
from .sub_agent.memory_info_agent.agent import memory_info_agent
from .sub_agent.disk_info_agent.agent import disk_info_agent
from .sub_agent.synatizer_agent.agent import synthesizer_agent


system_info_gather = ParallelAgent(
    name="system_info_gather",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
    description="You will analyze the system information"
)

root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[system_info_gather, synthesizer_agent]
)