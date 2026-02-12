"""
Memory agent - specialized for memory and artifact management.

This agent demonstrates:
- LoadArtifactsTool for loading saved files
- LoadMemoryTool for explicit memory search
- PreloadMemoryTool for automatic context injection
"""

from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools import (
    LoadArtifactsTool,
    LoadMemoryTool,
    PreloadMemoryTool,
)

from config.constants import (
    MEMORY_AGENT_NAME,
    MEMORY_INSTRUCTION,
    AGENT_DESCRIPTIONS,
)
from config.settings import get_settings
from tools.memory_tools import (
    get_load_artifacts_tool,
    get_load_memory_tool,
    get_preload_memory_tool,
    get_all_memory_tools,
)


# Local instruction variable
memory_system_instruction = """You are a memory management specialist responsible for managing conversation history and saved artifacts.

Your capabilities include:

Memory Operations:
- Search past conversations for relevant information
- Load specific memories based on queries
- Preload context for other agents

Artifact Operations:
- Load saved files and documents
- Retrieve specific artifacts by name
- List available artifacts

Guidelines:
1. Efficiently search and retrieve relevant memories
2. Organize information clearly when presenting
3. Maintain context across interactions
4. Clean up unused resources when appropriate

When searching memories:
- Use specific, targeted queries
- Consider time context (recent vs. older)
- Summarize findings clearly
- Indicate confidence in retrieved information

When loading artifacts:
- Verify artifact existence before loading
- Handle missing artifacts gracefully
- Provide clear descriptions of loaded content
"""


def create_memory_agent(
    model: Optional[str] = None,
    auto_preload: bool = False,
) -> LlmAgent:
    """
    Create the memory management agent.
    
    The memory agent handles memory search and artifact management,
    allowing retrieval of past conversations and saved files.
    
    Args:
        model: Model to use. Defaults to settings.
        auto_preload: If True, include PreloadMemoryTool for automatic
                     context injection in every request.
    
    Returns:
        LlmAgent: The configured memory agent.
    
    Example:
        # Basic memory agent
        memory = create_memory_agent()
        
        # With automatic context preloading
        memory = create_memory_agent(auto_preload=True)
    """
    settings = get_settings()
    
    # Build tools list
    tools = [
        get_load_artifacts_tool(),
        get_load_memory_tool(),
    ]
    
    # Add preload tool if requested
    if auto_preload:
        tools.append(get_preload_memory_tool())
    
    return LlmAgent(
        name=MEMORY_AGENT_NAME,
        model=model or settings.models.default_model,
        description=AGENT_DESCRIPTIONS[MEMORY_AGENT_NAME],
        instruction=memory_system_instruction,  # Using local variable
        tools=tools,
        disallow_transfer_to_parent=False,
    )


# Pre-configured memory agent
# Using direct tool instantiation
memory_agent = LlmAgent(
    name=MEMORY_AGENT_NAME,
    model="gemini-2.5-flash",  # Direct string
    description="Manages memory operations including loading, searching, and preloading memories and artifacts.",
    instruction=MEMORY_INSTRUCTION,  # From constants
    tools=[
        LoadArtifactsTool(),  # Direct instantiation
        LoadMemoryTool(),      # Direct instantiation
        # PreloadMemoryTool not included - use create_memory_agent(auto_preload=True)
    ],
)
