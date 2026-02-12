"""
Retry plugins for Google ADK.

Provides automatic retry functionality with reflection:
- ReflectAndRetryToolPlugin: Retries failed tool calls with reflection

This plugin helps recover from transient errors and improves
tool call success rates.
"""

from typing import Optional

from google.adk.plugins import ReflectAndRetryToolPlugin


def create_retry_plugin(
    max_retries: int = 3,
) -> ReflectAndRetryToolPlugin:
    """
    Create a reflect-and-retry plugin for tool failures.
    
    The ReflectAndRetryToolPlugin automatically retries failed tool
    calls with reflection. When a tool call fails, it:
    1. Analyzes the failure
    2. Reflects on what went wrong
    3. Retries with adjusted parameters
    
    Args:
        max_retries: Maximum number of retry attempts.
    
    Returns:
        ReflectAndRetryToolPlugin: A configured retry plugin.
    
    Example:
        plugin = create_retry_plugin(max_retries=5)
        agent = LlmAgent(
            name="resilient_agent",
            plugins=[plugin]
        )
    
    Use cases:
        - Transient API failures
        - Rate limiting recovery
        - Parameter validation errors
        - Network timeouts
    """
    return ReflectAndRetryToolPlugin(
        max_retries=max_retries,
    )


# Pre-configured retry plugin with default settings
retry_plugin = ReflectAndRetryToolPlugin(
    max_retries=3,  # Direct value
)


# Alternative configuration with higher retry limit
aggressive_retry_plugin = ReflectAndRetryToolPlugin(
    max_retries=5,
)


"""
Plugin Usage Patterns
=====================

1. Single Plugin
----------------
agent = LlmAgent(
    name="my_agent",
    plugins=[LoggingPlugin()]
)

2. Multiple Plugins
-------------------
Plugins are applied in order. Consider the order for logging/debugging.

agent = LlmAgent(
    name="my_agent",
    plugins=[
        LoggingPlugin(),           # Log first
        ReflectAndRetryToolPlugin(), # Then retry
        DebugLoggingPlugin(),      # Debug last (captures retries)
    ]
)

3. Conditional Plugin Application
---------------------------------
Use different plugins for development vs production.

if is_development:
    plugins = [DebugLoggingPlugin("debug.yaml")]
else:
    plugins = [LoggingPlugin()]

agent = LlmAgent(
    name="my_agent",
    plugins=plugins
)

4. Plugin on Orchestrator Only
------------------------------
Apply plugins to root agent to capture all activity.

orchestrator = LlmAgent(
    name="orchestrator",
    plugins=[LoggingPlugin()],  # Logs all agent activity
    sub_agents=[child1, child2]  # Children don't need plugins
)

5. Retry with Logging
---------------------
Combine retry with logging to track retry behavior.

agent = LlmAgent(
    name="resilient_agent",
    plugins=[
        LoggingPlugin(),
        ReflectAndRetryToolPlugin(max_retries=3),
    ]
)
"""
