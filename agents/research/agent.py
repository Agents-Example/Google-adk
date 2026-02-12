"""
Research agent - specialized for web search and information retrieval.

This agent demonstrates:
- Using built-in Gemini tools (GoogleSearchTool, UrlContextTool)
- Vertex AI Search integration
- MCP toolset integration for additional capabilities
- Bypass multi-tools limit for combining built-in tools with others
"""

from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools import (
    GoogleSearchTool,
    UrlContextTool,
    VertexAiSearchTool,
    FunctionTool,
)

from config.constants import (
    RESEARCH_AGENT_NAME,
    RESEARCH_INSTRUCTION,
    AGENT_DESCRIPTIONS,
    DEFAULT_MODEL,
)
from config.settings import get_settings
from tools.builtin_tools import (
    get_google_search_tool,
    get_url_context_tool,
    get_vertex_ai_search_tool,
)
from tools.custom_functions import fetch_url_content


def create_research_agent(
    model: Optional[str] = None,
    include_vertex_search: bool = True,
    include_mcp: bool = False,
) -> LlmAgent:
    """
    Create the research agent.
    
    The research agent specializes in web search and information retrieval
    using built-in Gemini tools and optionally Vertex AI Search.
    
    Args:
        model: Model to use. Defaults to settings.
        include_vertex_search: Include Vertex AI Search tool if configured.
        include_mcp: Include MCP filesystem tool for local document search.
    
    Returns:
        LlmAgent: The configured research agent.
    
    Example:
        # Basic research agent
        research = create_research_agent()
        
        # With Vertex AI Search
        research = create_research_agent(include_vertex_search=True)
    """
    settings = get_settings()
    
    # Build tools list
    tools = []
    
    # Add Google Search with bypass for multi-tool usage
    tools.append(get_google_search_tool(bypass_multi_tools_limit=True))
    
    # Add URL Context tool
    tools.append(get_url_context_tool())
    
    # Add custom URL fetcher as function tool
    tools.append(FunctionTool(fetch_url_content))
    
    # Add Vertex AI Search if configured and requested
    if include_vertex_search:
        if settings.vertex_search.data_store_id or settings.vertex_search.engine_id:
            tools.append(get_vertex_ai_search_tool(bypass_multi_tools_limit=True))
    
    # Add MCP tools if requested
    if include_mcp:
        from tools.mcp_tools import get_stdio_mcp_toolset
        try:
            mcp_toolset = get_stdio_mcp_toolset(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
                tool_filter=["read_file", "list_directory"],
            )
            tools.append(mcp_toolset)
        except Exception:
            pass  # MCP not available
    
    return LlmAgent(
        name=RESEARCH_AGENT_NAME,
        model=model or settings.models.default_model,
        description=AGENT_DESCRIPTIONS[RESEARCH_AGENT_NAME],
        instruction=RESEARCH_INSTRUCTION,  # Using constant
        tools=tools,
        # Allow returning to orchestrator
        disallow_transfer_to_parent=False,
    )


# Pre-configured research agent with direct instantiation
# Demonstrates inline tool configuration
research_agent = LlmAgent(
    name=RESEARCH_AGENT_NAME,
    model="gemini-2.5-flash",  # Direct string
    description="Specializes in web research, search operations, and information retrieval.",
    instruction="""You are a research specialist with powerful search capabilities.

Your tools include:
- Google Search for web searches
- URL Context for retrieving content from URLs
- Custom URL fetcher for detailed content retrieval

Research Guidelines:
1. Use Google Search for broad information gathering
2. Use URL Context to deep dive into specific pages
3. Cross-reference multiple sources when possible
4. Provide clear citations for your findings
5. Summarize key findings concisely

When researching:
- Start with broad searches to understand the topic
- Narrow down to specific sources
- Verify information across multiple sources
- Present findings in a clear, organized manner
""",  # Direct instruction string
    tools=[
        GoogleSearchTool(bypass_multi_tools_limit=True),  # Direct instantiation
        UrlContextTool(),  # Direct instantiation
        FunctionTool(fetch_url_content),  # Function tool for URL fetching
    ],
)
