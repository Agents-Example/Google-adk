"""Orchestrator agent module."""

from agents.orchestrator.agent import (
    create_orchestrator_agent,
    orchestrator_agent,
    build_multi_agent_system,
)
from agents.orchestrator.prompts import (
    ORCHESTRATOR_SYSTEM_INSTRUCTION,
    get_orchestrator_instruction,
)

__all__ = [
    "create_orchestrator_agent",
    "orchestrator_agent",
    "build_multi_agent_system",
    "ORCHESTRATOR_SYSTEM_INSTRUCTION",
    "get_orchestrator_instruction",
]
