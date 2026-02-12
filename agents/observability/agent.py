"""
Observability Agent - Demonstrates ALL observability integrations.

This agent shows how to USE all observability platforms:
- AgentOps: Session replays, metrics, monitoring
- Arize AX: Production-grade observability
- Phoenix: Open-source, self-hosted
- MLflow: OpenTelemetry trace ingestion
- Monocle: Open-source tracing
- Cloud Trace: Google Cloud native
- W&B Weave: Model call logging
- Freeplay: Testing and evaluation
"""

from typing import Optional
import os

from google.adk.agents import LlmAgent

from integrations.observability import (
    # AgentOps
    setup_agentops,
    agentops_config,
    # Arize AX
    setup_arize_ax,
    arize_ax_config,
    # Phoenix
    setup_phoenix,
    phoenix_config,
    # MLflow
    setup_mlflow,
    mlflow_config,
    # Monocle
    setup_monocle,
    monocle_config,
    # Cloud Trace
    setup_cloud_trace,
    cloud_trace_config,
    # Weave
    setup_weave,
    weave_config,
    # Freeplay
    setup_freeplay,
    freeplay_config,
)

from tools import get_sample_function_tools
from config import DEFAULT_MODEL


OBSERVABILITY_INSTRUCTION = """You are an Observability Agent that demonstrates ALL tracing and monitoring capabilities.

Your activities are traced by multiple observability platforms:

**AgentOps**: Session replays, metrics, and monitoring
- All agent runs, tool calls, and model requests are captured
- View traces at: https://app.agentops.ai

**Arize AX**: Production-grade observability
- Deep insights into agent behavior and LLM interactions
- Evaluation and experimentation capabilities

**Phoenix**: Open-source observability
- Self-hosted option for data privacy
- Comprehensive tracing and evaluation

**MLflow**: OpenTelemetry trace ingestion
- Standard OTEL traces for agent runs
- Integration with MLflow experiments

**Monocle**: Open-source tracing
- Automatic instrumentation
- VS Code extension for trace visualization

**Cloud Trace**: Google Cloud native
- Centralized tracing for cloud deployments
- Waterfall view of agent execution

**W&B Weave**: Model call logging
- Log and visualize model calls
- Timeline view of agent execution

When you respond, your actions are being traced across all configured platforms.
This enables comprehensive debugging, performance analysis, and improvement.
"""


def create_observability_agent(
    model: Optional[str] = None,
    observability_platform: str = "all",
) -> LlmAgent:
    """
    Create an agent with observability integrations.
    
    This demonstrates how to USE different observability platforms.
    
    Args:
        model: LLM model to use.
        observability_platform: Which platform to use ("all", "agentops", "phoenix", etc.)
    
    Returns:
        LlmAgent: Agent with observability configured.
    """
    # Setup observability based on platform selection
    if observability_platform == "all" or observability_platform == "agentops":
        if os.getenv("AGENTOPS_API_KEY"):
            setup_agentops(trace_name="observability-agent")
    
    if observability_platform == "all" or observability_platform == "arize":
        if os.getenv("ARIZE_API_KEY"):
            setup_arize_ax(project_name="observability-agent")
    
    if observability_platform == "all" or observability_platform == "phoenix":
        if os.getenv("PHOENIX_API_KEY"):
            setup_phoenix(project_name="observability-agent")
    
    if observability_platform == "all" or observability_platform == "mlflow":
        setup_mlflow(tracking_uri=mlflow_config.tracking_uri)
    
    if observability_platform == "all" or observability_platform == "monocle":
        setup_monocle(workflow_name="observability-agent")
    
    if observability_platform == "all" or observability_platform == "cloud_trace":
        if os.getenv("GOOGLE_CLOUD_PROJECT"):
            setup_cloud_trace()
    
    if observability_platform == "all" or observability_platform == "weave":
        if os.getenv("WANDB_API_KEY"):
            setup_weave(project_id="entity/observability-agent")
    
    if observability_platform == "all" or observability_platform == "freeplay":
        setup_freeplay()
    
    return LlmAgent(
        name="observability_agent",
        model=model or DEFAULT_MODEL,
        description="Agent with ALL observability integrations active",
        instruction=OBSERVABILITY_INSTRUCTION,
        tools=get_sample_function_tools(),
    )


# Pre-configured instance with Monocle (always available, no API key needed)
observability_agent = LlmAgent(
    name="observability_agent",
    model="gemini-2.5-flash",  # Direct string
    description="Agent demonstrating observability capabilities",
    instruction=OBSERVABILITY_INSTRUCTION,
    tools=get_sample_function_tools(),
)

# Setup Monocle by default (works without API keys)
setup_monocle(workflow_name="observability-agent")
