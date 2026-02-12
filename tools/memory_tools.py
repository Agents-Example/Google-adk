"""
Memory and artifact tools for Google ADK.

This module provides tools for memory and artifact management:
- LoadArtifactsTool: Load artifacts into session
- LoadMemoryTool: Load memory for user queries
- PreloadMemoryTool: Preload memory into LLM requests

These tools enable agents to access persistent storage and
historical context from past interactions.
"""

from typing import List

from google.adk.tools import (
    LoadArtifactsTool,
    LoadMemoryTool,
    PreloadMemoryTool,
    BaseTool,
)


def get_load_artifacts_tool() -> LoadArtifactsTool:
    """
    Create a LoadArtifactsTool.
    
    The LoadArtifactsTool loads artifacts from storage and adds them
    to the session. Artifacts are files identified by app name, user ID,
    session ID, and filename.
    
    Returns:
        LoadArtifactsTool: A configured artifact loading tool.
    
    Example:
        tool = get_load_artifacts_tool()
        # Agent can now request to load specific artifacts
        # "Load the report.pdf artifact"
    
    Usage in Agent:
        The tool allows the agent to request loading of previously
        saved artifacts. The LLM can call this tool with artifact
        identifiers to load them into the current context.
    """
    return LoadArtifactsTool()


def get_load_memory_tool() -> LoadMemoryTool:
    """
    Create a LoadMemoryTool.
    
    The LoadMemoryTool is a FunctionTool that loads memory for the
    current user based on a query. It searches the memory service
    and returns relevant past interactions.
    
    Returns:
        LoadMemoryTool: A configured memory loading tool.
    
    Example:
        tool = get_load_memory_tool()
        # Agent can now search memories
        # "What did we discuss about Python last week?"
    
    Note:
        Currently this tool only uses text parts from the memory.
        
    Usage in Agent:
        The tool exposes a `load_memory(query, tool_context)` function
        that the LLM can call to retrieve relevant memories based on
        a semantic query.
    """
    return LoadMemoryTool()


def get_preload_memory_tool() -> PreloadMemoryTool:
    """
    Create a PreloadMemoryTool.
    
    The PreloadMemoryTool preloads memory for the current user
    automatically for each LLM request. Unlike LoadMemoryTool,
    it won't be called by the model - it automatically executes
    to add context.
    
    Returns:
        PreloadMemoryTool: A configured memory preloading tool.
    
    Example:
        tool = get_preload_memory_tool()
        # Memory is automatically preloaded before each LLM call
    
    Note:
        Currently this tool only uses text parts from the memory.
        
    Usage in Agent:
        Add this tool to agents where you want past context to be
        automatically included in every request without the LLM
        needing to explicitly request it.
    """
    return PreloadMemoryTool()


def get_all_memory_tools() -> List[BaseTool]:
    """
    Get all memory and artifact tools.
    
    Returns a list of all memory-related tools for comprehensive
    memory management capabilities.
    
    Returns:
        List[BaseTool]: List of memory tools.
    
    Example:
        tools = get_all_memory_tools()
        memory_agent = LlmAgent(
            name="memory_manager",
            tools=tools
        )
    """
    return [
        get_load_artifacts_tool(),
        get_load_memory_tool(),
        get_preload_memory_tool(),
    ]


# Direct instantiation for variety in style

# Load artifacts tool - loads files from artifact storage
load_artifacts = LoadArtifactsTool()

# Load memory tool - explicit memory search by query
load_memory = LoadMemoryTool()

# Preload memory tool - automatic context injection
preload_memory = PreloadMemoryTool()


# Usage patterns documentation
"""
Memory Tools Usage Patterns
===========================

1. Explicit Memory Loading (LoadMemoryTool)
-------------------------------------------
Use when you want the agent to consciously decide when to access memories.

agent = LlmAgent(
    name="memory_aware_agent",
    instruction="You can search past conversations using the load_memory tool.",
    tools=[LoadMemoryTool()]
)

2. Automatic Memory Preloading (PreloadMemoryTool)
--------------------------------------------------
Use when you always want past context included without agent decision.

agent = LlmAgent(
    name="context_rich_agent",
    instruction="You have access to past conversation history.",
    tools=[PreloadMemoryTool()]  # Automatically adds context
)

3. Artifact Management (LoadArtifactsTool)
------------------------------------------
Use when agents need to access saved files like reports, images, etc.

agent = LlmAgent(
    name="document_agent",
    instruction="You can load saved documents using the load_artifacts tool.",
    tools=[LoadArtifactsTool()]
)

4. Combined Memory Strategy
---------------------------
Use multiple tools for comprehensive memory management.

agent = LlmAgent(
    name="full_memory_agent",
    instruction="You have access to memories and artifacts.",
    tools=[
        PreloadMemoryTool(),    # Automatic context
        LoadMemoryTool(),       # Explicit search
        LoadArtifactsTool(),    # File access
    ]
)

Memory Service Integration
--------------------------
Memory tools require a memory service to be configured in the runner:

runner = Runner(
    agent=agent,
    session_service=session_service,
    memory_service=memory_service,  # Required for memory tools
)

Artifact Service Integration
----------------------------
Artifact tools require an artifact service:

runner = Runner(
    agent=agent,
    session_service=session_service,
    artifact_service=artifact_service,  # Required for artifact tools
)
"""
