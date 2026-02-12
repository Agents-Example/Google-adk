"""
Function tools for Google ADK.

This module provides utilities for creating function-based tools:
- FunctionTool: Wrap Python functions as tools
- LongRunningFunctionTool: For async long-running operations
- AuthenticatedFunctionTool: For functions requiring authentication

These tools wrap user-defined Python functions and expose them
to the LLM as callable tools.
"""

from typing import Callable, Optional, List, Union, Dict, Any

from google.adk.tools import (
    FunctionTool,
    LongRunningFunctionTool,
    AuthenticatedFunctionTool,
    BaseTool,
)
from google.adk.auth import AuthConfig

from tools.custom_functions import (
    calculate_expression,
    get_current_time,
    format_text,
    fetch_url_content,
    analyze_sentiment,
    long_running_task,
    authenticated_api_call,
    process_with_context,
    tool_with_confirmation,
)


def create_function_tool(
    func: Callable,
    require_confirmation: Union[bool, Callable] = False,
) -> FunctionTool:
    """
    Create a FunctionTool from a Python function.
    
    FunctionTool wraps user-defined Python functions, extracting
    metadata from the function signature and docstring.
    
    Args:
        func: The Python function to wrap.
        require_confirmation: Whether the tool requires user confirmation.
                            Can be a boolean or a callable that takes
                            the function's arguments and returns a boolean.
    
    Returns:
        FunctionTool: A tool wrapping the function.
    
    Example:
        def my_function(x: int, y: int) -> int:
            '''Add two numbers.'''
            return x + y
        
        tool = create_function_tool(my_function)
    """
    return FunctionTool(func, require_confirmation=require_confirmation)


def create_long_running_function_tool(func: Callable) -> LongRunningFunctionTool:
    """
    Create a LongRunningFunctionTool from a Python function.
    
    LongRunningFunctionTool is for operations that may take significant
    time to complete. The framework will call the function, and once
    it returns, the response is returned asynchronously.
    
    Args:
        func: The Python function to wrap.
    
    Returns:
        LongRunningFunctionTool: A tool for long-running operations.
    
    Example:
        async def process_large_file(file_path: str) -> dict:
            '''Process a large file asynchronously.'''
            # Long-running processing...
            return {"status": "completed"}
        
        tool = create_long_running_function_tool(process_large_file)
    """
    return LongRunningFunctionTool(func)


def create_authenticated_function_tool(
    func: Callable,
    auth_config: Optional[AuthConfig] = None,
    response_for_auth_required: Optional[Dict[str, Any]] = None,
) -> AuthenticatedFunctionTool:
    """
    Create an AuthenticatedFunctionTool from a Python function.
    
    AuthenticatedFunctionTool handles authentication before the actual
    tool logic gets called. Functions can accept a special 'credential'
    argument which is the ready-to-use credential.
    
    Args:
        func: The Python function to wrap. Should accept a 'credential'
              parameter that will be populated with the auth credential.
        auth_config: Authentication configuration.
        response_for_auth_required: Response to return when auth is needed.
    
    Returns:
        AuthenticatedFunctionTool: A tool with authentication handling.
    
    Example:
        async def call_api(endpoint: str, credential=None) -> dict:
            '''Call an API with authentication.'''
            # Use credential for API call...
            return {"result": "data"}
        
        tool = create_authenticated_function_tool(
            func=call_api,
            auth_config=my_auth_config
        )
    """
    return AuthenticatedFunctionTool(
        func=func,
        auth_config=auth_config,
        response_for_auth_required=response_for_auth_required,
    )


def get_sample_function_tools() -> List[BaseTool]:
    """
    Get a collection of sample function tools.
    
    These demonstrate various patterns for function tools including:
    - Simple synchronous functions
    - Async functions
    - Functions with tool context
    - Functions requiring confirmation
    
    Returns:
        List[BaseTool]: List of sample function tools.
    
    Example:
        tools = get_sample_function_tools()
        agent = LlmAgent(
            name="function_demo",
            tools=tools
        )
    """
    tools = []
    
    # Simple synchronous function tools
    tools.append(FunctionTool(calculate_expression))
    tools.append(FunctionTool(get_current_time))
    tools.append(FunctionTool(format_text))
    tools.append(FunctionTool(analyze_sentiment))
    
    # Async function tool
    tools.append(FunctionTool(fetch_url_content))
    
    # Function with tool context
    tools.append(FunctionTool(process_with_context))
    
    # Tool with confirmation (static)
    tools.append(
        FunctionTool(
            tool_with_confirmation,
            require_confirmation=True
        )
    )
    
    # Long-running function tool
    tools.append(LongRunningFunctionTool(long_running_task))
    
    return tools


def get_authenticated_function_tools(
    auth_config: Optional[AuthConfig] = None,
) -> List[BaseTool]:
    """
    Get authenticated function tools.
    
    Args:
        auth_config: The authentication configuration to use.
    
    Returns:
        List[BaseTool]: List of authenticated function tools.
    """
    tools = []
    
    # Authenticated API call tool
    tools.append(
        AuthenticatedFunctionTool(
            func=authenticated_api_call,
            auth_config=auth_config,
            response_for_auth_required={
                "status": "auth_required",
                "message": "Please authenticate to use this tool"
            }
        )
    )
    
    return tools


# Pre-configured tool instances for direct use
# These use direct inline definitions (as requested for variety)

calculator_tool = FunctionTool(calculate_expression)
"""A calculator tool for evaluating mathematical expressions."""

time_tool = FunctionTool(get_current_time)
"""A tool for getting the current time in various formats and timezones."""

text_formatter_tool = FunctionTool(format_text)
"""A tool for formatting text with various operations."""

sentiment_analyzer_tool = FunctionTool(analyze_sentiment)
"""A tool for analyzing sentiment in text."""

url_fetcher_tool = FunctionTool(fetch_url_content)
"""A tool for fetching content from URLs."""

long_task_tool = LongRunningFunctionTool(long_running_task)
"""A long-running task tool for async operations."""

# Tool with dynamic confirmation based on action type
dangerous_action_tool = FunctionTool(
    tool_with_confirmation,
    require_confirmation=lambda args: args.get("action") in ["delete", "modify", "reset"]
)
"""A tool that requires confirmation for dangerous actions."""
