"""
Orchestrator agent - the root agent for the multi-agent system.

The orchestrator analyzes user requests and delegates to specialized
agents using the TransferToAgentTool. It demonstrates:
- LlmAgent configuration with various options
- TransferToAgentTool for agent-to-agent communication
- Sub-agent registration
- Callback integration
"""

from typing import Optional, List

from google.adk.agents import LlmAgent, Agent
from google.adk.tools import TransferToAgentTool, AgentTool

from config.constants import (
    DEFAULT_MODEL,
    ORCHESTRATOR_AGENT_NAME,
    AGENT_DESCRIPTIONS,
    RESEARCH_AGENT_NAME,
    CODE_AGENT_NAME,
    DATA_AGENT_NAME,
    INTEGRATION_AGENT_NAME,
    MEMORY_AGENT_NAME,
    SEQUENTIAL_PIPELINE_NAME,
    PARALLEL_SEARCH_NAME,
    LOOP_REFINEMENT_NAME,
)
from config.settings import get_settings
from agents.orchestrator.prompts import (
    ORCHESTRATOR_SYSTEM_INSTRUCTION,
    get_orchestrator_instruction,
)


def create_orchestrator_agent(
    sub_agents: Optional[List[LlmAgent]] = None,
    model: Optional[str] = None,
    use_dynamic_instruction: bool = False,
) -> LlmAgent:
    """
    Create the orchestrator agent.
    
    The orchestrator is the root agent that coordinates all other agents.
    It uses TransferToAgentTool to delegate tasks to specialized agents.
    
    Args:
        sub_agents: List of sub-agents to register.
        model: Model to use. Defaults to DEFAULT_MODEL.
        use_dynamic_instruction: If True, use dynamic instruction generation.
    
    Returns:
        LlmAgent: The configured orchestrator agent.
    
    Example:
        # Basic orchestrator
        orchestrator = create_orchestrator_agent()
        
        # With sub-agents
        orchestrator = create_orchestrator_agent(
            sub_agents=[research_agent, code_agent]
        )
    """
    settings = get_settings()
    
    # Determine instruction style
    if use_dynamic_instruction:
        # Dynamic instruction using function
        instruction = get_orchestrator_instruction(
            available_agents=[
                RESEARCH_AGENT_NAME,
                CODE_AGENT_NAME,
                DATA_AGENT_NAME,
                INTEGRATION_AGENT_NAME,
                MEMORY_AGENT_NAME,
            ]
        )
    else:
        # Direct constant instruction
        instruction = ORCHESTRATOR_SYSTEM_INSTRUCTION
    
    # Get agent names for TransferToAgentTool
    agent_names = [
        RESEARCH_AGENT_NAME,
        CODE_AGENT_NAME,
        DATA_AGENT_NAME,
        INTEGRATION_AGENT_NAME,
        MEMORY_AGENT_NAME,
        SEQUENTIAL_PIPELINE_NAME,
        PARALLEL_SEARCH_NAME,
        LOOP_REFINEMENT_NAME,
    ]
    
    # Create transfer tool with enum constraints
    transfer_tool = TransferToAgentTool(agent_names=agent_names)
    
    return LlmAgent(
        name=ORCHESTRATOR_AGENT_NAME,
        model=model or settings.models.default_model,  # Using settings variable
        description=AGENT_DESCRIPTIONS[ORCHESTRATOR_AGENT_NAME],  # Using constant variable
        instruction=instruction,
        tools=[transfer_tool],
        sub_agents=sub_agents or [],
        # Allow transfer back to parent (root has no parent)
        disallow_transfer_to_parent=False,
        # Allow transfer to peer agents
        disallow_transfer_to_peers=False,
    )


def build_multi_agent_system() -> LlmAgent:
    """
    Build the complete multi-agent system.
    
    This function assembles all agents into a hierarchical structure
    with the orchestrator as the root agent.
    
    Returns:
        LlmAgent: The root orchestrator with all sub-agents configured.
    
    Example:
        root_agent = build_multi_agent_system()
        runner = Runner(
            agent=root_agent,
            session_service=session_service
        )
    """
    # Import here to avoid circular imports
    from agents.research.agent import create_research_agent
    from agents.code_execution.agent import create_code_agent
    from agents.data_analysis.agent import create_data_agent
    from agents.integration.agent import create_integration_agent
    from agents.memory.agent import create_memory_agent
    from agents.workflows.sequential import create_sequential_pipeline
    from agents.workflows.parallel import create_parallel_search
    from agents.workflows.loop import create_loop_refinement
    
    # Create all specialized agents
    research = create_research_agent()
    code = create_code_agent()
    data = create_data_agent()
    integration = create_integration_agent()
    memory = create_memory_agent()
    
    # Create workflow agents
    sequential = create_sequential_pipeline()
    parallel = create_parallel_search()
    loop = create_loop_refinement()
    
    # Create orchestrator with all sub-agents
    orchestrator = create_orchestrator_agent(
        sub_agents=[
            research,
            code,
            data,
            integration,
            memory,
            sequential,
            parallel,
            loop,
        ]
    )
    
    return orchestrator


# Pre-configured orchestrator instance
# Uses direct model string (variety in approach)
orchestrator_agent = LlmAgent(
    name=ORCHESTRATOR_AGENT_NAME,
    model="gemini-2.5-flash",  # Direct model string
    description="The main orchestrator that coordinates all other agents.",
    instruction=ORCHESTRATOR_SYSTEM_INSTRUCTION,  # Using constant
    tools=[
        TransferToAgentTool(agent_names=[
            RESEARCH_AGENT_NAME,
            CODE_AGENT_NAME,
            DATA_AGENT_NAME,
            INTEGRATION_AGENT_NAME,
            MEMORY_AGENT_NAME,
        ])
    ],
    # These can be populated later
    sub_agents=[],
)
