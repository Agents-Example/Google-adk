"""
Tools module for Google ADK Multi-Agent System.

This module provides all tool configurations and instances including:
- Built-in Gemini tools (GoogleSearch, UrlContext, etc.)
- Function tools (FunctionTool, LongRunningFunctionTool, etc.)
- Google API toolsets (Calendar, Gmail, Sheets, etc.)
- MCP tools and toolsets
- OpenAPI tools
- Enterprise tools (APIHub, Application Integration)
- Memory and artifact tools
- Custom function definitions
"""

# Built-in tools
from tools.builtin_tools import (
    get_google_search_tool,
    get_url_context_tool,
    get_vertex_ai_search_tool,
    get_google_maps_grounding_tool,
    get_enterprise_web_search_tool,
    get_discovery_engine_search_tool,
    get_all_builtin_tools,
)

# Function tools
from tools.function_tools import (
    create_function_tool,
    create_long_running_function_tool,
    create_authenticated_function_tool,
    get_sample_function_tools,
)

# Google API toolsets
from tools.google_api_tools import (
    get_calendar_toolset,
    get_gmail_toolset,
    get_docs_toolset,
    get_sheets_toolset,
    get_slides_toolset,
    get_youtube_toolset,
    get_bigquery_toolset,
    get_all_google_api_toolsets,
)

# MCP tools
from tools.mcp_tools import (
    get_stdio_mcp_toolset,
    get_sse_mcp_toolset,
    get_http_mcp_toolset,
    get_api_registry_toolset,
    get_all_mcp_toolsets,
)

# OpenAPI tools
from tools.openapi_tools import (
    create_openapi_toolset,
    create_rest_api_tool,
    get_sample_openapi_toolset,
)

# Enterprise tools
from tools.enterprise_tools import (
    get_apihub_toolset,
    get_application_integration_toolset,
    get_toolbox_toolset,
    get_all_enterprise_toolsets,
)

# Memory tools
from tools.memory_tools import (
    get_load_artifacts_tool,
    get_load_memory_tool,
    get_preload_memory_tool,
    get_all_memory_tools,
)

# Custom functions for FunctionTool
from tools.custom_functions import (
    calculate_expression,
    get_current_time,
    format_text,
    fetch_url_content,
    analyze_sentiment,
    long_running_task,
    authenticated_api_call,
)

__all__ = [
    # Built-in tools
    "get_google_search_tool",
    "get_url_context_tool",
    "get_vertex_ai_search_tool",
    "get_google_maps_grounding_tool",
    "get_enterprise_web_search_tool",
    "get_discovery_engine_search_tool",
    "get_all_builtin_tools",
    # Function tools
    "create_function_tool",
    "create_long_running_function_tool",
    "create_authenticated_function_tool",
    "get_sample_function_tools",
    # Google API toolsets
    "get_calendar_toolset",
    "get_gmail_toolset",
    "get_docs_toolset",
    "get_sheets_toolset",
    "get_slides_toolset",
    "get_youtube_toolset",
    "get_bigquery_toolset",
    "get_all_google_api_toolsets",
    # MCP tools
    "get_stdio_mcp_toolset",
    "get_sse_mcp_toolset",
    "get_http_mcp_toolset",
    "get_api_registry_toolset",
    "get_all_mcp_toolsets",
    # OpenAPI tools
    "create_openapi_toolset",
    "create_rest_api_tool",
    "get_sample_openapi_toolset",
    # Enterprise tools
    "get_apihub_toolset",
    "get_application_integration_toolset",
    "get_toolbox_toolset",
    "get_all_enterprise_toolsets",
    # Memory tools
    "get_load_artifacts_tool",
    "get_load_memory_tool",
    "get_preload_memory_tool",
    "get_all_memory_tools",
    # Custom functions
    "calculate_expression",
    "get_current_time",
    "format_text",
    "fetch_url_content",
    "analyze_sentiment",
    "long_running_task",
    "authenticated_api_call",
]
