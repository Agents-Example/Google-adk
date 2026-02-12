"""
MCP (Model Context Protocol) tools for Google ADK.

This module provides MCP integration including:
- McpToolset: Connect to MCP servers and use their tools
- StdioConnectionParams: For local MCP servers (npx, python)
- SseConnectionParams: For SSE-based MCP servers
- StreamableHTTPConnectionParams: For HTTP-based MCP servers
- ApiRegistry: For MCP servers from API Registry
- McpInstructionProvider: Fetch instructions from MCP servers

MCP enables standardized communication with external tool servers.
"""

from typing import Optional, List, Dict, Any, Callable

from mcp import StdioServerParameters

from google.adk.tools.mcp_tool import (
    McpToolset,
    McpTool,
    StdioConnectionParams,
    SseConnectionParams,
    StreamableHTTPConnectionParams,
)
from google.adk.tools import ApiRegistry
from google.adk.agents import McpInstructionProvider
from google.adk.tools.base_toolset import BaseToolset, ToolPredicate
from google.adk.agents.callback_context import ReadonlyContext

from config.settings import get_settings


def get_stdio_mcp_toolset(
    command: Optional[str] = None,
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: float = 5.0,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
    tool_name_prefix: Optional[str] = None,
) -> McpToolset:
    """
    Create an MCP toolset using stdio connection (local server).
    
    The stdio connection is used for local MCP servers that run as
    subprocesses, such as those started with npx or python.
    
    Args:
        command: Command to run the MCP server (e.g., "npx", "python").
        args: Arguments for the command.
        env: Environment variables for the subprocess.
        timeout: Connection timeout in seconds.
        tool_filter: Filter to select specific tools.
        tool_name_prefix: Prefix for tool names.
    
    Returns:
        McpToolset: A configured MCP toolset.
    
    Example:
        # Filesystem MCP server
        toolset = get_stdio_mcp_toolset(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        )
        
        # Python MCP server
        toolset = get_stdio_mcp_toolset(
            command="python",
            args=["-m", "my_mcp_server"]
        )
    """
    settings = get_settings()
    
    # Use defaults from settings
    command = command or settings.mcp.stdio_command
    args = args or settings.mcp.stdio_args
    
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=command,
                args=args,
                env=env,
            ),
            timeout=timeout,
        ),
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
    )


def get_sse_mcp_toolset(
    url: Optional[str] = None,
    headers: Optional[Dict[str, Any]] = None,
    timeout: float = 5.0,
    sse_read_timeout: float = 300.0,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
    tool_name_prefix: Optional[str] = None,
    header_provider: Optional[Callable[[ReadonlyContext], Dict[str, str]]] = None,
) -> McpToolset:
    """
    Create an MCP toolset using SSE connection (remote server).
    
    The SSE connection is used for remote MCP servers that communicate
    via Server-Sent Events.
    
    Args:
        url: URL of the SSE MCP server.
        headers: Static headers for the connection.
        timeout: Connection timeout in seconds.
        sse_read_timeout: Read timeout for SSE events.
        tool_filter: Filter to select specific tools.
        tool_name_prefix: Prefix for tool names.
        header_provider: Dynamic header provider function.
    
    Returns:
        McpToolset: A configured MCP toolset.
    
    Example:
        toolset = get_sse_mcp_toolset(
            url="http://localhost:8080/sse",
            headers={"Authorization": "Bearer token"}
        )
    """
    settings = get_settings()
    
    url = url or settings.mcp.sse_url
    if not url:
        raise ValueError("SSE URL is required. Set MCP_SSE_URL in environment.")
    
    return McpToolset(
        connection_params=SseConnectionParams(
            url=url,
            headers=headers,
            timeout=timeout,
            sse_read_timeout=sse_read_timeout,
        ),
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
        header_provider=header_provider,
    )


def get_http_mcp_toolset(
    url: Optional[str] = None,
    headers: Optional[Dict[str, Any]] = None,
    timeout: float = 5.0,
    sse_read_timeout: float = 300.0,
    terminate_on_close: bool = True,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
    tool_name_prefix: Optional[str] = None,
    header_provider: Optional[Callable[[ReadonlyContext], Dict[str, str]]] = None,
) -> McpToolset:
    """
    Create an MCP toolset using Streamable HTTP connection.
    
    The Streamable HTTP connection provides bidirectional streaming
    over HTTP for MCP servers.
    
    Args:
        url: URL of the HTTP MCP server.
        headers: Static headers for the connection.
        timeout: Connection timeout in seconds.
        sse_read_timeout: Read timeout for streaming.
        terminate_on_close: Whether to terminate server on close.
        tool_filter: Filter to select specific tools.
        tool_name_prefix: Prefix for tool names.
        header_provider: Dynamic header provider function.
    
    Returns:
        McpToolset: A configured MCP toolset.
    
    Example:
        toolset = get_http_mcp_toolset(
            url="http://localhost:8080/mcp",
            timeout=10.0
        )
    """
    settings = get_settings()
    
    url = url or settings.mcp.http_url
    if not url:
        raise ValueError("HTTP URL is required. Set MCP_HTTP_URL in environment.")
    
    return McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=url,
            headers=headers,
            timeout=timeout,
            sse_read_timeout=sse_read_timeout,
            terminate_on_close=terminate_on_close,
        ),
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
        header_provider=header_provider,
    )


def get_api_registry_toolset(
    api_registry_project_id: str,
    mcp_server_name: str,
    location: str = "global",
    tool_filter: Optional[List[str] | ToolPredicate] = None,
    tool_name_prefix: Optional[str] = None,
    header_provider: Optional[Callable] = None,
) -> McpToolset:
    """
    Get MCP toolset from API Registry.
    
    The ApiRegistry class provides McpToolsets for MCP servers
    registered in Google Cloud API Registry.
    
    Args:
        api_registry_project_id: GCP project ID for API Registry.
        mcp_server_name: Name of the MCP server in the registry.
        location: Location of API Registry resources.
        tool_filter: Filter to select specific tools.
        tool_name_prefix: Prefix for tool names.
        header_provider: Function to provide headers for MCP calls.
    
    Returns:
        McpToolset: A configured MCP toolset from API Registry.
    
    Example:
        toolset = get_api_registry_toolset(
            api_registry_project_id="my-project",
            mcp_server_name="my-mcp-server"
        )
    """
    registry = ApiRegistry(
        api_registry_project_id=api_registry_project_id,
        location=location,
        header_provider=header_provider,
    )
    
    return registry.get_toolset(
        mcp_server_name=mcp_server_name,
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
    )


def get_mcp_instruction_provider(
    connection_params,
    prompt_name: str,
) -> McpInstructionProvider:
    """
    Create an MCP instruction provider.
    
    The McpInstructionProvider fetches agent instructions from an MCP server.
    This allows dynamic instruction loading from external sources.
    
    Args:
        connection_params: MCP connection parameters.
        prompt_name: Name of the MCP Prompt to fetch.
    
    Returns:
        McpInstructionProvider: A configured instruction provider.
    
    Example:
        instruction_provider = get_mcp_instruction_provider(
            connection_params=SseConnectionParams(url="http://..."),
            prompt_name="agent_instructions"
        )
        
        agent = LlmAgent(
            name="mcp_instructed",
            instruction=instruction_provider
        )
    """
    return McpInstructionProvider(
        connection_params=connection_params,
        prompt_name=prompt_name,
    )


def get_all_mcp_toolsets() -> List[McpToolset]:
    """
    Get all configured MCP toolsets.
    
    Returns toolsets for all MCP connection types that are configured
    in the environment.
    
    Returns:
        List[McpToolset]: List of available MCP toolsets.
    
    Note:
        Only returns toolsets for which connection parameters are configured.
        Empty list if no MCP servers are configured.
    """
    settings = get_settings()
    toolsets = []
    
    # Stdio toolset (always available with defaults)
    try:
        toolsets.append(get_stdio_mcp_toolset(
            tool_name_prefix="stdio_"
        ))
    except Exception:
        pass
    
    # SSE toolset (if configured)
    if settings.mcp.sse_url:
        try:
            toolsets.append(get_sse_mcp_toolset(
                tool_name_prefix="sse_"
            ))
        except Exception:
            pass
    
    # HTTP toolset (if configured)
    if settings.mcp.http_url:
        try:
            toolsets.append(get_http_mcp_toolset(
                tool_name_prefix="http_"
            ))
        except Exception:
            pass
    
    return toolsets


# Direct MCP toolset instantiation examples (for variety)
# These demonstrate inline configuration style

# Example: Filesystem MCP server with StdioConnectionParams
filesystem_mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
        ),
        timeout=10.0,
    ),
    tool_filter=["read_file", "write_file", "list_directory"],
    tool_name_prefix="fs_",
)

# Example: Custom header provider for dynamic auth
def dynamic_auth_header_provider(ctx: ReadonlyContext) -> Dict[str, str]:
    """
    Provides dynamic authentication headers based on context.
    
    This function is called for each MCP request to provide
    current authentication tokens.
    """
    # In production, retrieve token from context state or auth service
    token = ctx.state.get("auth_token", "default-token")
    return {
        "Authorization": f"Bearer {token}",
        "X-Request-ID": ctx.state.get("request_id", "unknown"),
    }
