"""
Agents module for Google ADK Multi-Agent System.

This module provides all agent definitions including:
- Orchestrator: Root agent with transfer capabilities
- Research: Search and information retrieval
- Code Execution: Code running with executors
- Data Analysis: BigQuery and data tools
- Integration: Google API integrations
- Memory: Memory and artifact management
- Workflows: Sequential, Parallel, and Loop agents
- Comprehensive: Agent using ALL plugins, services, integrations
- MCP Hub: Agent with ALL MCP integrations
- Observability: Agent with ALL observability platforms
"""

# Orchestrator
from agents.orchestrator.agent import (
    create_orchestrator_agent,
    orchestrator_agent,
)

# Research
from agents.research.agent import (
    create_research_agent,
    research_agent,
)

# Code Execution
from agents.code_execution.agent import (
    create_code_agent,
    code_execution_agent,
)

# Data Analysis
from agents.data_analysis.agent import (
    create_data_agent,
    data_analysis_agent,
)

# Integration
from agents.integration.agent import (
    create_integration_agent,
    integration_agent,
)

# Memory
from agents.memory.agent import (
    create_memory_agent,
    memory_agent,
)

# Workflows
from agents.workflows.sequential import (
    create_sequential_pipeline,
    sequential_pipeline,
)
from agents.workflows.parallel import (
    create_parallel_search,
    parallel_search,
)
from agents.workflows.loop import (
    create_loop_refinement,
    loop_refinement,
)

# Comprehensive Agent - USES all plugins, services, integrations
from agents.comprehensive.agent import (
    create_comprehensive_agent,
    comprehensive_agent,
)

# MCP Hub Agent - ALL MCP integrations
from agents.mcp_hub.agent import (
    create_mcp_hub_agent,
    mcp_hub_agent,
)

# Observability Agent - ALL observability platforms
from agents.observability.agent import (
    create_observability_agent,
    observability_agent,
)

# Build complete multi-agent system
from agents.orchestrator.agent import build_multi_agent_system

__all__ = [
    # Orchestrator
    "create_orchestrator_agent",
    "orchestrator_agent",
    # Research
    "create_research_agent",
    "research_agent",
    # Code
    "create_code_agent",
    "code_execution_agent",
    # Data
    "create_data_agent",
    "data_analysis_agent",
    # Integration
    "create_integration_agent",
    "integration_agent",
    # Memory
    "create_memory_agent",
    "memory_agent",
    # Workflows
    "create_sequential_pipeline",
    "sequential_pipeline",
    "create_parallel_search",
    "parallel_search",
    "create_loop_refinement",
    "loop_refinement",
    # Comprehensive (uses ALL plugins, services, integrations)
    "create_comprehensive_agent",
    "comprehensive_agent",
    # MCP Hub (ALL MCP integrations)
    "create_mcp_hub_agent",
    "mcp_hub_agent",
    # Observability (ALL observability platforms)
    "create_observability_agent",
    "observability_agent",
    # Multi-agent system
    "build_multi_agent_system",
]
