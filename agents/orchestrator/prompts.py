"""
Prompts for the orchestrator agent.

Demonstrates different ways to provide instructions:
- Direct string constants
- Dynamic instruction functions
- Template-based instructions
"""

from typing import Optional
from config.constants import ORCHESTRATOR_INSTRUCTION


# Direct string constant approach
ORCHESTRATOR_SYSTEM_INSTRUCTION = """You are the central orchestrator for a sophisticated multi-agent AI system.

Your primary responsibilities:
1. Analyze incoming user requests to understand their intent and requirements
2. Determine which specialized agent or workflow is best suited to handle each request
3. Use the transfer_to_agent tool to delegate tasks to the appropriate agent
4. Coordinate complex tasks that may require multiple agents working together
5. Provide helpful responses when you can directly assist without delegation

Available Specialized Agents:
- research_agent: Expert in web search, information retrieval, and research tasks
  Use for: Searching the web, finding information, fact-checking, retrieving URL content

- code_execution_agent: Expert in code execution, analysis, and generation
  Use for: Running Python code, analyzing code, debugging, generating code solutions

- data_analysis_agent: Expert in data analysis and BigQuery operations
  Use for: Database queries, data analysis, generating insights from data

- integration_agent: Expert in Google API integrations
  Use for: Calendar operations, Gmail, Google Docs, Sheets, Slides, YouTube

- memory_agent: Expert in memory and artifact management
  Use for: Retrieving past conversations, managing saved files, loading context

Available Workflow Agents:
- sequential_pipeline: Multi-stage data processing pipeline
  Use for: Tasks requiring ordered processing steps (collect → process → report)

- parallel_search: Concurrent multi-source search
  Use for: Tasks benefiting from searching multiple sources simultaneously

- loop_refinement: Iterative improvement workflow
  Use for: Tasks requiring multiple refinement passes until quality is satisfactory

Decision Guidelines:
- Always choose the most specific agent for the task
- For ambiguous requests, ask clarifying questions
- For complex tasks, consider which workflow agent might be appropriate
- If you can handle a simple request directly, do so without delegation
"""


def get_orchestrator_instruction(
    available_agents: Optional[list[str]] = None,
    custom_context: Optional[str] = None,
) -> str:
    """
    Generate dynamic orchestrator instruction.
    
    This function demonstrates the InstructionProvider pattern where
    instructions can be generated dynamically based on context.
    
    Args:
        available_agents: List of available agent names to include.
        custom_context: Additional context to add to the instruction.
    
    Returns:
        str: The generated instruction.
    
    Example:
        # Dynamic instruction
        instruction = get_orchestrator_instruction(
            available_agents=["research_agent", "code_agent"],
            custom_context="Focus on code-related tasks today."
        )
        
        agent = LlmAgent(
            name="orchestrator",
            instruction=instruction
        )
    """
    base_instruction = ORCHESTRATOR_INSTRUCTION
    
    if available_agents:
        agents_str = "\n".join(f"- {agent}" for agent in available_agents)
        base_instruction += f"\n\nCurrently available agents:\n{agents_str}"
    
    if custom_context:
        base_instruction += f"\n\nAdditional Context:\n{custom_context}"
    
    return base_instruction


# Template-based instruction with placeholders
ORCHESTRATOR_TEMPLATE = """You are {agent_role} for the {system_name} system.

Your primary task is to {primary_task}.

You have access to the following agents:
{agent_list}

Remember to:
{guidelines}
"""


def get_templated_instruction(
    agent_role: str = "the central orchestrator",
    system_name: str = "multi-agent AI",
    primary_task: str = "analyze requests and delegate to appropriate agents",
    agents: Optional[dict[str, str]] = None,
    guidelines: Optional[list[str]] = None,
) -> str:
    """
    Generate instruction from template.
    
    This demonstrates a template-based approach to instruction generation.
    
    Args:
        agent_role: Role description for the agent.
        system_name: Name of the system.
        primary_task: Primary task description.
        agents: Dict of agent names to descriptions.
        guidelines: List of guidelines.
    
    Returns:
        str: The generated instruction from template.
    """
    default_agents = {
        "research_agent": "Web search and information retrieval",
        "code_execution_agent": "Code execution and analysis",
        "data_analysis_agent": "Data analysis and BigQuery",
        "integration_agent": "Google API integrations",
        "memory_agent": "Memory and artifact management",
    }
    
    default_guidelines = [
        "Choose the most appropriate agent for each task",
        "Ask clarifying questions when the request is ambiguous",
        "Provide direct responses for simple queries",
        "Consider workflow agents for complex multi-step tasks",
    ]
    
    agents = agents or default_agents
    guidelines = guidelines or default_guidelines
    
    agent_list = "\n".join(f"- {name}: {desc}" for name, desc in agents.items())
    guidelines_str = "\n".join(f"- {g}" for g in guidelines)
    
    return ORCHESTRATOR_TEMPLATE.format(
        agent_role=agent_role,
        system_name=system_name,
        primary_task=primary_task,
        agent_list=agent_list,
        guidelines=guidelines_str,
    )
