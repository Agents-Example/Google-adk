"""
Custom Python functions for use with FunctionTool.

These functions demonstrate various patterns that can be wrapped
with FunctionTool, LongRunningFunctionTool, or AuthenticatedFunctionTool.

Includes:
- Simple synchronous functions
- Async functions
- Functions with ToolContext
- Long-running operations
- Functions requiring authentication
"""

import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
import json


def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: A mathematical expression to evaluate.
                   Supports +, -, *, /, **, (), and common math functions.
    
    Returns:
        Dict containing the result or error message.
    
    Example:
        result = calculate_expression("2 + 2 * 3")
        # Returns: {"result": 8, "expression": "2 + 2 * 3"}
    """
    import math
    
    # Safe evaluation with limited scope
    allowed_names = {
        "abs": abs, "round": round, "min": min, "max": max,
        "sum": sum, "pow": pow,
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
        "tan": math.tan, "log": math.log, "log10": math.log10,
        "exp": math.exp, "pi": math.pi, "e": math.e,
    }
    
    try:
        # Evaluate expression in restricted namespace
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return {
            "result": result,
            "expression": expression,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "expression": expression,
            "status": "error"
        }


def get_current_time(
    timezone: Optional[str] = None,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> Dict[str, str]:
    """
    Get the current time.
    
    Args:
        timezone: Optional timezone name (e.g., "UTC", "US/Eastern").
                 Defaults to local timezone.
        format: strftime format string.
    
    Returns:
        Dict with formatted time and timezone info.
    
    Example:
        result = get_current_time(timezone="UTC")
        # Returns: {"time": "2024-01-15 10:30:00", "timezone": "UTC"}
    """
    try:
        from zoneinfo import ZoneInfo
        
        if timezone:
            tz = ZoneInfo(timezone)
            now = datetime.now(tz)
        else:
            now = datetime.now()
            timezone = "local"
        
        return {
            "time": now.strftime(format),
            "timezone": timezone,
            "iso": now.isoformat(),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }


def format_text(
    text: str,
    operation: str = "uppercase",
    **kwargs
) -> Dict[str, str]:
    """
    Format text with various operations.
    
    Args:
        text: The text to format.
        operation: One of: uppercase, lowercase, title, reverse, 
                  word_count, char_count, strip, replace.
        **kwargs: Additional arguments for specific operations.
    
    Returns:
        Dict with formatted text and operation info.
    
    Example:
        result = format_text("Hello World", operation="uppercase")
        # Returns: {"result": "HELLO WORLD", "operation": "uppercase"}
    """
    operations = {
        "uppercase": lambda t, **kw: t.upper(),
        "lowercase": lambda t, **kw: t.lower(),
        "title": lambda t, **kw: t.title(),
        "reverse": lambda t, **kw: t[::-1],
        "word_count": lambda t, **kw: str(len(t.split())),
        "char_count": lambda t, **kw: str(len(t)),
        "strip": lambda t, **kw: t.strip(),
        "replace": lambda t, **kw: t.replace(kw.get("old", ""), kw.get("new", "")),
    }
    
    if operation not in operations:
        return {
            "error": f"Unknown operation: {operation}",
            "available": list(operations.keys()),
            "status": "error"
        }
    
    try:
        result = operations[operation](text, **kwargs)
        return {
            "result": result,
            "operation": operation,
            "original": text,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }


async def fetch_url_content(
    url: str,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Fetch content from a URL asynchronously.
    
    This is an async function demonstrating how ADK handles async tools.
    
    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.
    
    Returns:
        Dict with URL content or error.
    
    Example:
        result = await fetch_url_content("https://example.com")
    """
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                content = await response.text()
                return {
                    "url": url,
                    "status_code": response.status,
                    "content_length": len(content),
                    "content_preview": content[:500] + "..." if len(content) > 500 else content,
                    "status": "success"
                }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "status": "error"
        }


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of text (mock implementation).
    
    This is a placeholder that demonstrates the function signature.
    In production, you would integrate with a real sentiment analysis API.
    
    Args:
        text: The text to analyze.
    
    Returns:
        Dict with sentiment analysis results.
    
    Example:
        result = analyze_sentiment("I love this product!")
        # Returns: {"sentiment": "positive", "confidence": 0.95, ...}
    """
    # Mock sentiment analysis
    # In production, integrate with Google Cloud Natural Language API
    # or another sentiment analysis service
    
    positive_words = {"good", "great", "excellent", "love", "happy", "amazing"}
    negative_words = {"bad", "terrible", "hate", "sad", "awful", "horrible"}
    
    words = set(text.lower().split())
    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)
    
    if pos_count > neg_count:
        sentiment = "positive"
        confidence = min(0.5 + pos_count * 0.1, 0.99)
    elif neg_count > pos_count:
        sentiment = "negative"
        confidence = min(0.5 + neg_count * 0.1, 0.99)
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "word_count": len(text.split()),
        "status": "success"
    }


async def long_running_task(
    task_name: str,
    duration_seconds: int = 5,
    tool_context=None,
) -> Dict[str, Any]:
    """
    A long-running task for demonstrating LongRunningFunctionTool.
    
    This simulates a task that takes significant time to complete,
    such as processing a large file or making multiple API calls.
    
    Args:
        task_name: Name of the task for identification.
        duration_seconds: How long the task should run.
        tool_context: The tool context (provided by ADK).
    
    Returns:
        Dict with task results.
    
    Example:
        # Wrapped with LongRunningFunctionTool
        tool = LongRunningFunctionTool(long_running_task)
    """
    # Simulate long-running work
    await asyncio.sleep(duration_seconds)
    
    return {
        "task_name": task_name,
        "duration_seconds": duration_seconds,
        "completed_at": datetime.now().isoformat(),
        "status": "completed",
        "result": f"Task '{task_name}' completed successfully after {duration_seconds}s"
    }


async def authenticated_api_call(
    endpoint: str,
    method: str = "GET",
    credential=None,  # Populated by AuthenticatedFunctionTool
    tool_context=None,
) -> Dict[str, Any]:
    """
    Make an authenticated API call.
    
    This demonstrates how AuthenticatedFunctionTool provides credentials.
    The 'credential' parameter is automatically populated by ADK with
    the ready-to-use authentication credential.
    
    Args:
        endpoint: The API endpoint to call.
        method: HTTP method (GET, POST, etc.).
        credential: Auth credential (populated by ADK).
        tool_context: The tool context (provided by ADK).
    
    Returns:
        Dict with API response or error.
    
    Example:
        # Wrapped with AuthenticatedFunctionTool
        tool = AuthenticatedFunctionTool(
            func=authenticated_api_call,
            auth_config=auth_config
        )
    """
    if credential is None:
        return {
            "error": "No credential provided",
            "status": "auth_required"
        }
    
    # Mock API call - in production, use the credential to authenticate
    return {
        "endpoint": endpoint,
        "method": method,
        "credential_type": type(credential).__name__ if credential else None,
        "response": {
            "message": "Mock API response",
            "data": {"example": "data"}
        },
        "status": "success"
    }


def process_with_context(
    data: str,
    tool_context,
) -> Dict[str, Any]:
    """
    Process data using tool context.
    
    Demonstrates accessing tool_context for:
    - Session state
    - Artifacts
    - Memory search
    - Event actions
    
    Args:
        data: Data to process.
        tool_context: The ToolContext from ADK.
    
    Returns:
        Dict with processing results.
    """
    # Access session state
    state = tool_context.state
    
    # Access function call ID
    function_call_id = tool_context.function_call_id
    
    # Access actions for modifying state
    actions = tool_context.actions
    
    return {
        "data": data,
        "function_call_id": function_call_id,
        "session_state_keys": list(state.to_dict().keys()) if hasattr(state, 'to_dict') else [],
        "status": "success"
    }


def tool_with_confirmation(
    action: str,
    target: str,
    tool_context,
) -> Dict[str, Any]:
    """
    A tool that requests user confirmation before proceeding.
    
    Demonstrates the require_confirmation feature of FunctionTool.
    
    Args:
        action: The action to perform (e.g., "delete", "modify").
        target: The target of the action.
        tool_context: The ToolContext from ADK.
    
    Returns:
        Dict with action results.
    
    Example:
        # With static confirmation requirement
        tool = FunctionTool(tool_with_confirmation, require_confirmation=True)
        
        # With dynamic confirmation based on action
        tool = FunctionTool(
            tool_with_confirmation,
            require_confirmation=lambda args: args.get("action") == "delete"
        )
    """
    return {
        "action": action,
        "target": target,
        "confirmed": True,
        "result": f"Successfully performed {action} on {target}",
        "status": "success"
    }
