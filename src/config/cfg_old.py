import os
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
import toml

from dotenv import load_dotenv
load_dotenv(verbose=True)

from src.utils import assemble_project_path

class WebSearchToolConfig(BaseModel):
    engine: Optional[str] = Field(default=None,
                                  description="Search engine the llm to use")
    fallback_engines: Optional[List[str]] = Field(default=None,
                                                  description="Fallback search engines to try if the primary engine fails")
    retry_delay: Optional[int] = Field(default=None,
                                       description="Seconds to wait before retrying all engines again after they all fail")
    max_retries: Optional[int] = Field(default=None,
                                       description="Maximum number of times to retry all engines when all fail")
    lang: Optional[str] = Field(default=None,
                                description="Language code for search results (e.g., en, zh, fr)")
    country: Optional[str] = Field(default=None,
                                   description="Country code for search results (e.g., us, cn, uk)")
    filter_year: Optional[int] = Field(default=None,
                                       description="Filter results by year (0 for no filter)")
    num_results: Optional[int] = Field(default=None,
                                       description="Number of search results to return")
    fetch_content: Optional[bool]= Field(default=None,
                                         description="Whether to fetch content from the search results")
    max_length: Optional[int] = Field(default=None,
                                      description="Maximum character length for the content to be fetched")

class DeepResearcherToolConfig(BaseModel):
    model_id: Optional[str] = Field(default=None,
                                    description="Model ID for the LLM to use")
    max_depth: Optional[int] = Field(default=None,
                                     description="Maximum depth for the search")
    max_insights: Optional[int] = Field(default=None,
                                        description="Maximum number of insights to extract")
    time_limit_seconds: Optional[int] = Field(default=None,
                                              description="Time limit for the search in seconds")
    max_follow_ups: Optional[int] = Field(default=None,
                                          description="Maximum number of follow-up questions to ask")

class BrowserToolConfig(BaseModel):
    model_id: Optional[str] = Field(default=None,
                                    description="Model ID for the LLM to use")
    headless: Optional[bool] = Field(default=None,
                                     description="Whether to run browser in headless mode")
    disable_security: Optional[bool] = Field(default=None,
                                             description="Disable browser security features")
    extra_chromium_args: Optional[List[str]] = Field(default=None,
                                                     description="Extra arguments to pass to the browser")
    chrome_instance_path: Optional[str] = Field(default=None,
                                                description="Path to a Chrome instance to use")
    wss_url: Optional[str] = Field(default=MemoryError,
                                   description="Connect to a browser instance via WebSocket")
    cdp_url: Optional[str] = Field(default=None,
                                   description="Connect to a browser instance via CDP")
    use_proxy: Optional[bool] = Field(default=None,
                                      description="Whether to use a proxy")
    proxy: Optional[Dict[str, Any]] = Field(default = None,
                                            description="Proxy settings for the browser")
    max_length: Optional[int] = Field(default=None,
                                      description="Maximum character length for the content to be fetched")

class DeepAnalyzerToolConfig(BaseModel):
    analyzer_model_ids: Optional[List[str]] = Field(default = None,
                                                    description="Model IDs for the LLMs to use")
    summarizer_model_id: Optional[str] = Field(default=None,
                                               description="Model ID for the LLM to use")
class AgentConfig(BaseModel):
    model_id: str = Field(default="gpt-4.1",
                          description="Model ID for the LLM to use")
    name: str = Field(default="agent", 
                      description="Name of the agent")
    description: str = Field(default="A multi-step agent that can perform various tasks.", 
                             description="Description of the agent")
    max_steps: int = Field(default=20, 
                           description="Maximum number of steps the agent can take")
    template_path: str = Field(default="", 
                               description="Path to the template file for the agent")
    tools: List[str] = Field(default_factory=lambda: [],
                            description="List of tools the agent can use")
    mcp_tools: List[str] = Field(default_factory=lambda: [],
                                description="List of MCP tools the agent can use")
    managed_agents: List[str] = Field(default_factory=lambda: [], 
                                      description="List of agents the agent can manage")

class HierarchicalAgentConfig(BaseModel):
    name: str = Field(default="dra", description="Name of the hierarchical agent")
    use_hierarchical_agent: bool = Field(default=True, description="Whether to use hierarchical agent")

    general_agent_config: AgentConfig = Field(default_factory=lambda: AgentConfig(
        model_id="gpt-4.1",
        name="general_agent",
        description="A general agent that can perform various tasks and manage other agents.",
        max_steps=20,
        template_path=assemble_project_path("src/agent/general_agent/prompts/general_agent.yaml"),
        tools=["python_interpreter"],
        mcp_tools=["get_weather"],
    ))
    planning_agent_config: AgentConfig = Field(default_factory=lambda: AgentConfig(
        model_id="gpt-4.1",
        name="planning_agent",
        description="A planning agent that can plan the steps to complete the task.",
        max_steps=20,
        template_path=assemble_project_path("src/agent/planning_agent/prompts/planning_agent.yaml"),
        tools=['planning'],
        mcp_tools=[],
        managed_agents=["deep_analyzer_agent", "browser_use_agent", "deep_researcher_agent"],
    ))
    deep_analyzer_agent_config: AgentConfig = Field(default_factory=lambda: AgentConfig(
        model_id="gpt-4.1",
        name="deep_analyzer_agent",
        description="A team member that that performs systematic, step-by-step analysis of a given task, optionally leveraging information from external resources such as attached file or uri to provide comprehensive reasoning and answers. For any tasks that require in-depth analysis, particularly those involving attached file or uri, game, chess, computational tasks, or any other complex tasks. Please ask him for the reasoning and the final answer.",
        max_steps=3,
        template_path=assemble_project_path("src/agent/deep_analyzer_agent/prompts/deep_analyzer_agent.yaml"),
        tools=["deep_analyzer", "python_interpreter"],
        mcp_tools=[],
    ))
    browser_use_agent_config: AgentConfig = Field(default_factory=lambda: AgentConfig(
        model_id="gpt-4.1",
        name="browser_use_agent",
        description="A team member that can search the most relevant web pages and interact with them to find answers to tasks, specializing in precise information retrieval and accurate page-level interactions. Please ask this member to get the answers from the web when high accuracy and detailed extraction are required.",
        max_steps=5,
        template_path=assemble_project_path("src/agent/browser_use_agent/prompts/browser_use_agent.yaml"),
        tools=["auto_browser_use", "python_interpreter"],
        mcp_tools=[],
    ))
    deep_researcher_agent_config: AgentConfig = Field(default_factory=lambda: AgentConfig(
        model_id="gpt-4.1",
        name="deep_researcher_agent",
        description="A team member capable of conducting extensive web searches to complete tasks, primarily focused on retrieving broad and preliminary information for quickly understanding a topic or obtaining rough answers. For tasks that require precise, structured, or interactive page-level information retrieval, please use the `browser_use_agent`.",
        max_steps=3,
        template_path=assemble_project_path("src/agent/deep_researcher_agent/prompts/deep_researcher_agent.yaml"),
        tools=["deep_researcher", "python_interpreter"],
        mcp_tools=[],
    ))

class DatasetConfig(BaseModel):
    name: str = Field(default="2023_all", description="Dataset name")
    path: str = Field(default=assemble_project_path("data/GAIA"), description="Path to the dataset")

class Config(BaseModel):
    
    # General Config
    workdir: str = "workdir"
    tag: str = f"agentscope"
    concurrency: int = 4
    log_path: str = 'log.txt'
    download_path: str = 'downloads_folder'
    use_local_proxy: bool = Field(default=True, description="Whether to use local proxy")
    split: str = Field(default="validation", description="Set name")
    save_path: str = Field(default="agentscope.jsonl", description="Path to save the answers")
    
    # Tool Config
    web_search_tool: WebSearchToolConfig = Field(default_factory=WebSearchToolConfig)
    deep_researcher_tool: DeepResearcherToolConfig = Field(default_factory=DeepResearcherToolConfig)
    browser_tool: BrowserToolConfig = Field(default_factory=BrowserToolConfig)
    deep_analyzer_tool: DeepAnalyzerToolConfig = Field(default_factory=DeepAnalyzerToolConfig)
    mcp_tools: Dict[str, Any] = Field(default = {
        "mcpServers": {
            # Local stdio server
            "get_weather": {
                "command": "python",
                "args": [str(assemble_project_path("src/mcp/server.py"))],
                "env": {"DEBUG": "true"}
            },
            # Remote server
            # "calendar": {
            #     "url": "https://calendar-api.example.com/mcp",
            #     "transport": "streamable-http"
            # }
        }
    })
    
    # Agent Config
    agent: HierarchicalAgentConfig = Field(default_factory=HierarchicalAgentConfig)
    
    # Dataset Config
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    
    def init_config(self, config_path: "config.toml"):
        
        with open(config_path, "r") as f:
            config = toml.load(f)
            
        # General Config
        self.workdir = config["workdir"]
        self.tag = config["tag"]
        self.concurrency = config["concurrency"]
        self.log_path = config["log_path"]
        self.download_path = config["download_path"]
        self.use_local_proxy = config["use_local_proxy"]
        self.split = config["split"]
        self.save_path = config["save_path"]
        
        # Create Workdir
        self.workdir = assemble_project_path(os.path.join('workdir', self.tag))
        os.makedirs(self.workdir, exist_ok=True)
        self.log_path = os.path.join(self.workdir, 'log.txt')
        self.download_path = os.path.join(self.workdir, 'downloads_folder')
        os.makedirs(self.download_path, exist_ok=True)
        self.save_path = os.path.join(self.workdir, self.save_path)
            
        # Tool Config
        self.web_search_tool = WebSearchToolConfig(**config["web_search_tool"])
        self.deep_researcher_tool = DeepResearcherToolConfig(**config["deep_researcher_tool"])
        self.browser_tool = BrowserToolConfig(**config["browser_tool"])
        self.deep_analyzer_tool = DeepAnalyzerToolConfig(**config["deep_analyzer_tool"])

        # Agent Config
        general_agent_config = AgentConfig(**config["agent"]["general_agent_config"])
        general_agent_config.template_path = assemble_project_path(config["agent"]["general_agent_config"]["template_path"])
        planning_agent_config = AgentConfig(**config["agent"]["planning_agent_config"])
        planning_agent_config.template_path = assemble_project_path(config["agent"]["planning_agent_config"]["template_path"])
        deep_analyzer_agent_config = AgentConfig(**config["agent"]["deep_analyzer_agent_config"])
        deep_analyzer_agent_config.template_path = assemble_project_path(config["agent"]["deep_analyzer_agent_config"]["template_path"])
        browser_use_agent_config = AgentConfig(**config["agent"]["browser_use_agent_config"])
        browser_use_agent_config.template_path = assemble_project_path(config["agent"]["browser_use_agent_config"]["template_path"])
        deep_researcher_agent_config = AgentConfig(**config["agent"]["deep_researcher_agent_config"])
        deep_researcher_agent_config.template_path = assemble_project_path(config["agent"]["deep_researcher_agent_config"]["template_path"])
        self.agent = HierarchicalAgentConfig(
            name=config["agent"]["name"],
            use_hierarchical_agent=config["agent"]["use_hierarchical_agent"],
            general_agent_config=general_agent_config,
            planning_agent_config=planning_agent_config,
            deep_analyzer_agent_config=deep_analyzer_agent_config,
            browser_use_agent_config=browser_use_agent_config,
            deep_researcher_agent_config=deep_researcher_agent_config,
        ) 
        
        # Dataset Config
        self.dataset = DatasetConfig(**config["dataset"])
        
    def __str__(self):
        return self.model_dump_json(indent=4)

config = Config()