"""
Examples module for Google ADK Multi-Agent System.

This module provides example tools and providers:
- ExampleTool: Tool that provides example outputs
- BaseExampleProvider: Base class for example providers

Examples help guide agent behavior by showing expected outputs.
"""

from examples.example_tool import (
    create_example_tool,
    example_tool,
    ExampleProvider,
)

__all__ = [
    "create_example_tool",
    "example_tool",
    "ExampleProvider",
]
