"""
Tool callbacks for Google ADK.

Tool callbacks are invoked before and after tool execution.
They can be used for:
- Logging tool calls
- Modifying tool inputs/outputs
- Implementing access control
- Auditing tool usage
"""

from typing import Optional, Dict, Any
import logging

from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)


def sample_before_tool_callback(
    tool_context: ToolContext,
    tool_name: str,
    tool_args: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Sample before-tool callback.
    
    This callback is invoked before a tool is executed.
    It can be used to:
    - Log tool invocations
    - Validate tool arguments
    - Modify tool arguments
    - Block tool execution
    
    Args:
        tool_context: Context with tool execution info.
        tool_name: Name of the tool being called.
        tool_args: Arguments passed to the tool.
    
    Returns:
        Optional[Dict]: Modified arguments, or None to use original.
                       Return {"_skip": True} to skip tool execution.
    
    Example:
        agent = LlmAgent(
            name="my_agent",
            before_tool_callback=sample_before_tool_callback
        )
    """
    logger.info(f"Before tool '{tool_name}' with args: {tool_args}")
    
    # Return None to use original arguments
    return None


def sample_after_tool_callback(
    tool_context: ToolContext,
    tool_name: str,
    tool_args: Dict[str, Any],
    tool_response: Any,
) -> Optional[Any]:
    """
    Sample after-tool callback.
    
    This callback is invoked after a tool completes execution.
    It can be used to:
    - Log tool results
    - Modify tool output
    - Audit tool usage
    
    Args:
        tool_context: Context with tool execution info.
        tool_name: Name of the tool that was called.
        tool_args: Arguments passed to the tool.
        tool_response: Response from the tool.
    
    Returns:
        Optional[Any]: Modified response, or None to use original.
    
    Example:
        agent = LlmAgent(
            name="my_agent",
            after_tool_callback=sample_after_tool_callback
        )
    """
    logger.info(f"After tool '{tool_name}' - Response type: {type(tool_response)}")
    
    # Return None to use original response
    return None


def tool_logging_callback(
    tool_context: ToolContext,
    tool_name: str,
    tool_args: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Comprehensive logging callback for tools.
    """
    function_call_id = tool_context.function_call_id
    state = tool_context.state
    
    logger.info(
        f"[TOOL CALL] Tool: {tool_name} | "
        f"Call ID: {function_call_id} | "
        f"Args: {tool_args}"
    )
    
    return None


def access_control_callback(
    tool_context: ToolContext,
    tool_name: str,
    tool_args: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Access control callback to restrict tool usage.
    
    Demonstrates blocking certain tools or arguments.
    """
    # List of restricted tools
    restricted_tools = ["dangerous_tool", "admin_tool"]
    
    if tool_name in restricted_tools:
        # Check if user has permission
        user_role = tool_context.state.get("user_role", "guest")
        
        if user_role != "admin":
            logger.warning(f"Access denied to tool '{tool_name}' for role '{user_role}'")
            return {"_skip": True, "_reason": "Access denied"}
    
    return None


def argument_validation_callback(
    tool_context: ToolContext,
    tool_name: str,
    tool_args: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Validate and sanitize tool arguments.
    """
    # Example: Sanitize string arguments
    sanitized_args = {}
    for key, value in tool_args.items():
        if isinstance(value, str):
            # Basic sanitization - strip whitespace, limit length
            sanitized_args[key] = value.strip()[:10000]
        else:
            sanitized_args[key] = value
    
    return sanitized_args if sanitized_args != tool_args else None


def audit_callback_after(
    tool_context: ToolContext,
    tool_name: str,
    tool_args: Dict[str, Any],
    tool_response: Any,
) -> Optional[Any]:
    """
    Audit callback to log tool usage for compliance.
    """
    # In production, this might write to an audit log database
    audit_entry = {
        "tool": tool_name,
        "args": tool_args,
        "response_type": type(tool_response).__name__,
        "function_call_id": tool_context.function_call_id,
        # Add timestamp, user_id, etc. in production
    }
    
    logger.info(f"[AUDIT] {audit_entry}")
    
    return None


"""
Tool Callback Patterns
======================

1. Simple Logging
-----------------
agent = LlmAgent(
    name="logged_agent",
    before_tool_callback=tool_logging_callback,
    after_tool_callback=audit_callback_after
)

2. Access Control
-----------------
agent = LlmAgent(
    name="secure_agent",
    before_tool_callback=access_control_callback
)

3. Argument Modification
------------------------
def add_context_callback(ctx, name, args):
    args["context"] = {"user_id": ctx.state.get("user_id")}
    return args

agent = LlmAgent(
    name="contextual_agent",
    before_tool_callback=add_context_callback
)

4. Response Processing
----------------------
def mask_sensitive_callback(ctx, name, args, response):
    if "password" in str(response):
        return {"status": "success", "data": "[REDACTED]"}
    return None

agent = LlmAgent(
    name="privacy_agent",
    after_tool_callback=mask_sensitive_callback
)
"""
