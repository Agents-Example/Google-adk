"""
Built-in Gemini tools for Google ADK.

These are built-in tools that are automatically invoked by Gemini models
and do not require local code execution. They operate internally within
the model.

Includes:
- GoogleSearchTool: Web search grounding
- UrlContextTool: URL content retrieval
- VertexAiSearchTool: Vertex AI Search integration
- GoogleMapsGroundingTool: Maps-based grounding (Vertex AI only)
- EnterpriseWebSearchTool: Enterprise-compliant web search
- DiscoveryEngineSearchTool: Discovery Engine search
"""

from typing import List, Optional

from google.adk.tools import (
    GoogleSearchTool,
    UrlContextTool,
    VertexAiSearchTool,
    GoogleMapsGroundingTool,
    EnterpriseWebSearchTool,
    DiscoveryEngineSearchTool,
    BaseTool,
)

from config.settings import get_settings


def get_google_search_tool(
    bypass_multi_tools_limit: bool = False,
    model: Optional[str] = None,
) -> GoogleSearchTool:
    """
    Create a Google Search tool for web search grounding.
    
    The GoogleSearchTool is automatically invoked by Gemini 2 models
    to retrieve search results from Google Search. It operates internally
    within the model.
    
    Args:
        bypass_multi_tools_limit: Whether to bypass the multi-tools limitation
                                  so the tool can be used with other tools.
        model: Optional model name to use for processing the LLM request.
    
    Returns:
        GoogleSearchTool: A configured Google Search tool.
    
    Example:
        # Basic usage
        search_tool = get_google_search_tool()
        
        # With multi-tool bypass
        search_tool = get_google_search_tool(bypass_multi_tools_limit=True)
    """
    return GoogleSearchTool(
        bypass_multi_tools_limit=bypass_multi_tools_limit,
        model=model,
    )


def get_url_context_tool() -> UrlContextTool:
    """
    Create a URL Context tool for content retrieval.
    
    The UrlContextTool is automatically invoked by Gemini 2 models
    to retrieve content from URLs and use that content to inform
    and shape its response.
    
    Returns:
        UrlContextTool: A configured URL Context tool.
    
    Example:
        url_tool = get_url_context_tool()
        # Agent can now retrieve content from URLs mentioned in queries
    """
    return UrlContextTool()


def get_vertex_ai_search_tool(
    data_store_id: Optional[str] = None,
    search_engine_id: Optional[str] = None,
    filter: Optional[str] = None,
    max_results: Optional[int] = None,
    bypass_multi_tools_limit: bool = False,
) -> VertexAiSearchTool:
    """
    Create a Vertex AI Search tool.
    
    The VertexAiSearchTool integrates with Vertex AI Search for
    enterprise search capabilities. You can use either a data store
    or search engine.
    
    Args:
        data_store_id: Vertex AI Search data store resource ID.
                      Format: projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore}
        search_engine_id: Vertex AI Search engine resource ID.
                         Format: projects/{project}/locations/{location}/collections/{collection}/engines/{engine}
        filter: Optional filter for search results.
        max_results: Maximum number of results to return.
        bypass_multi_tools_limit: Whether to bypass multi-tools limitation.
    
    Returns:
        VertexAiSearchTool: A configured Vertex AI Search tool.
    
    Note:
        Either data_store_id or search_engine_id must be provided, not both.
    
    Example:
        # Using data store
        search_tool = get_vertex_ai_search_tool(
            data_store_id="projects/my-project/locations/global/..."
        )
        
        # Using search engine
        search_tool = get_vertex_ai_search_tool(
            search_engine_id="projects/my-project/locations/global/..."
        )
    """
    settings = get_settings()
    
    # Use settings if not provided
    if data_store_id is None and search_engine_id is None:
        data_store_id = settings.vertex_search.data_store_id
        search_engine_id = settings.vertex_search.engine_id
    
    return VertexAiSearchTool(
        data_store_id=data_store_id,
        search_engine_id=search_engine_id,
        filter=filter,
        max_results=max_results,
        bypass_multi_tools_limit=bypass_multi_tools_limit,
    )


def get_google_maps_grounding_tool() -> GoogleMapsGroundingTool:
    """
    Create a Google Maps Grounding tool.
    
    The GoogleMapsGroundingTool is automatically invoked by Gemini 2 models
    to ground query results with Google Maps. Only available for use with
    the Vertex AI Gemini API.
    
    Returns:
        GoogleMapsGroundingTool: A configured Maps grounding tool.
    
    Note:
        Requires GOOGLE_GENAI_USE_VERTEXAI=TRUE
    
    Example:
        maps_tool = get_google_maps_grounding_tool()
        # Agent can now ground location-based queries with Maps
    """
    return GoogleMapsGroundingTool()


def get_enterprise_web_search_tool() -> EnterpriseWebSearchTool:
    """
    Create an Enterprise Web Search tool.
    
    The EnterpriseWebSearchTool provides web grounding that is compliant
    with enterprise requirements. It uses Google's enterprise-grade
    web search infrastructure.
    
    Returns:
        EnterpriseWebSearchTool: A configured enterprise search tool.
    
    Note:
        Only available with Vertex AI Gemini API.
        This is different from Vertex AI Search (formerly "Enterprise Search").
    
    Example:
        enterprise_search = get_enterprise_web_search_tool()
    """
    return EnterpriseWebSearchTool()


def get_discovery_engine_search_tool(
    data_store_id: Optional[str] = None,
    search_engine_id: Optional[str] = None,
    filter: Optional[str] = None,
    max_results: Optional[int] = None,
) -> DiscoveryEngineSearchTool:
    """
    Create a Discovery Engine Search tool.
    
    The DiscoveryEngineSearchTool uses Vertex AI Search's discovery
    engine search API for searching through configured data stores.
    
    Args:
        data_store_id: Discovery Engine data store resource ID.
        search_engine_id: Discovery Engine search engine resource ID.
        filter: Optional filter for search results.
        max_results: Maximum number of results to return.
    
    Returns:
        DiscoveryEngineSearchTool: A configured discovery engine tool.
    
    Example:
        discovery_tool = get_discovery_engine_search_tool(
            data_store_id="projects/my-project/locations/global/..."
        )
    """
    settings = get_settings()
    
    return DiscoveryEngineSearchTool(
        data_store_id=data_store_id or settings.vertex_search.data_store_id,
        search_engine_id=search_engine_id or settings.vertex_search.engine_id,
        filter=filter,
        max_results=max_results,
    )


def get_all_builtin_tools(
    include_vertex_only: bool = False,
) -> List[BaseTool]:
    """
    Get all available built-in tools.
    
    Args:
        include_vertex_only: If True, includes tools that only work
                            with Vertex AI (Maps grounding, Enterprise search).
    
    Returns:
        List[BaseTool]: List of all built-in tools.
    
    Example:
        # Get tools for Google AI
        tools = get_all_builtin_tools()
        
        # Get all tools including Vertex AI only
        tools = get_all_builtin_tools(include_vertex_only=True)
    """
    tools = [
        get_google_search_tool(),
        get_url_context_tool(),
    ]
    
    # Add Vertex AI Search if configured
    settings = get_settings()
    if settings.vertex_search.data_store_id or settings.vertex_search.engine_id:
        tools.append(get_vertex_ai_search_tool())
        tools.append(get_discovery_engine_search_tool())
    
    # Add Vertex AI only tools
    if include_vertex_only:
        tools.append(get_google_maps_grounding_tool())
        tools.append(get_enterprise_web_search_tool())
    
    return tools
