"""
Callbacks module for Google ADK Multi-Agent System.

Callbacks provide hooks into agent, tool, and LLM execution:
- Agent callbacks: before/after agent execution
- Tool callbacks: before/after tool calls
- Model callbacks: before/after LLM calls

These allow customization of behavior without modifying agent code.
"""

from callbacks.agent_callbacks import (
    sample_before_agent_callback,
    sample_after_agent_callback,
    logging_before_agent,
    logging_after_agent,
)
from callbacks.tool_callbacks import (
    sample_before_tool_callback,
    sample_after_tool_callback,
    tool_logging_callback,
)
from callbacks.model_callbacks import (
    sample_before_model_callback,
    sample_after_model_callback,
    model_logging_callback,
)

__all__ = [
    # Agent callbacks
    "sample_before_agent_callback",
    "sample_after_agent_callback",
    "logging_before_agent",
    "logging_after_agent",
    # Tool callbacks
    "sample_before_tool_callback",
    "sample_after_tool_callback",
    "tool_logging_callback",
    # Model callbacks
    "sample_before_model_callback",
    "sample_after_model_callback",
    "model_logging_callback",
]
