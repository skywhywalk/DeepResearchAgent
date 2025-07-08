_base_ = './base.py'

# General Config
tag = "general"
concurrency = 4
workdir = "workdir"
log_path = "log.txt"
use_local_proxy = False # True for local proxy, False for public proxy

use_hierarchical_agent = False

general_agent_config = dict(
    type="general_agent",
    name="general_agent",
    model_id="gpt-4.1",
    description = "A general agent that can handle various tasks.",
    max_steps = 20,
    template_path = "src/agent/general_agent/prompts/general_agent.yaml",
    provide_run_summary = True,
    tools = ["python_interpreter_tool", "image_generator_tool", "video_generator_tool"],
    mcp_tools = ["get_weather_tool"],
)

agent_config = general_agent_config