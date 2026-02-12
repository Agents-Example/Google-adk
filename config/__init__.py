"""
Configuration module for Google ADK Multi-Agent System.

This module provides centralized configuration management including:
- Environment-based settings
- Shared constants
- Model configurations
- Agent naming conventions
"""

from config.settings import Settings, get_settings
from config.constants import (
    # Models
    DEFAULT_MODEL,
    THINKING_MODEL,
    GEMMA_MODEL,
    # Agent Names
    ORCHESTRATOR_AGENT_NAME,
    RESEARCH_AGENT_NAME,
    CODE_AGENT_NAME,
    DATA_AGENT_NAME,
    INTEGRATION_AGENT_NAME,
    MEMORY_AGENT_NAME,
    # Workflow Agent Names
    SEQUENTIAL_PIPELINE_NAME,
    PARALLEL_SEARCH_NAME,
    LOOP_REFINEMENT_NAME,
    # Descriptions
    AGENT_DESCRIPTIONS,
)

__all__ = [
    # Settings
    "Settings",
    "get_settings",
    # Models
    "DEFAULT_MODEL",
    "THINKING_MODEL",
    "GEMMA_MODEL",
    # Agent Names
    "ORCHESTRATOR_AGENT_NAME",
    "RESEARCH_AGENT_NAME",
    "CODE_AGENT_NAME",
    "DATA_AGENT_NAME",
    "INTEGRATION_AGENT_NAME",
    "MEMORY_AGENT_NAME",
    # Workflow Names
    "SEQUENTIAL_PIPELINE_NAME",
    "PARALLEL_SEARCH_NAME",
    "LOOP_REFINEMENT_NAME",
    # Descriptions
    "AGENT_DESCRIPTIONS",
]
