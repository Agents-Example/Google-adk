"""
Logging plugins for Google ADK.

Provides plugins for logging agent execution:
- LoggingPlugin: Basic logging of agent/tool calls
- DebugLoggingPlugin: Detailed debug output to YAML file

These plugins help with monitoring, debugging, and auditing
agent behavior.
"""

from typing import Optional

from google.adk.plugins import (
    LoggingPlugin,
    DebugLoggingPlugin,
)

from config.settings import get_settings


def create_logging_plugin() -> LoggingPlugin:
    """
    Create a basic logging plugin.
    
    The LoggingPlugin logs agent and tool executions to standard
    Python logging. Useful for monitoring and basic debugging.
    
    Returns:
        LoggingPlugin: A configured logging plugin.
    
    Example:
        plugin = create_logging_plugin()
        agent = LlmAgent(
            name="my_agent",
            plugins=[plugin]
        )
    
    What it logs:
        - Agent invocations (before/after)
        - Tool calls (before/after)
        - Model calls (before/after)
        - Errors and exceptions
    """
    return LoggingPlugin()


def create_debug_logging_plugin(
    output_path: Optional[str] = None,
) -> DebugLoggingPlugin:
    """
    Create a debug logging plugin.
    
    The DebugLoggingPlugin writes detailed execution information
    to a YAML file for comprehensive debugging.
    
    Args:
        output_path: Path for the debug output file.
                    Defaults to settings.debug.output_path.
    
    Returns:
        DebugLoggingPlugin: A configured debug logging plugin.
    
    Example:
        plugin = create_debug_logging_plugin("debug_session.yaml")
        agent = LlmAgent(
            name="my_agent",
            plugins=[plugin]
        )
    
    Output includes:
        - Full request/response content
        - Token usage statistics
        - Timing information
        - Tool call details
        - Error stack traces
    """
    settings = get_settings()
    
    return DebugLoggingPlugin(
        output_path=output_path or settings.debug.output_path
    )


# Pre-configured plugin instances

# Basic logging plugin
logging_plugin = LoggingPlugin()

# Debug logging plugin with default output path
settings = get_settings()
debug_logging_plugin = DebugLoggingPlugin(
    output_path=settings.debug.output_path  # From settings
)
