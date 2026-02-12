"""
Observability integrations for Google ADK.

Provides setup functions and configurations for all observability platforms:
- AgentOps: Session replays, metrics, and monitoring
- Arize AX: Production-grade observability and evaluation
- Phoenix: Open-source, self-hosted observability
- MLflow: OpenTelemetry trace ingestion
- Monocle: Open-source tracing and debugging
- Cloud Trace: Google Cloud native tracing
- W&B Weave: Log, visualize, and analyze model calls
- Freeplay: Testing and evaluation platform
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


# =============================================================================
# AgentOps Integration
# =============================================================================

@dataclass
class AgentOpsConfig:
    """Configuration for AgentOps integration."""
    api_key: Optional[str] = None
    trace_name: str = "adk-app-trace"
    auto_start_session: bool = True
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("AGENTOPS_API_KEY")


agentops_config = AgentOpsConfig()


def setup_agentops(
    api_key: Optional[str] = None,
    trace_name: str = "adk-app-trace",
    auto_start_session: bool = True,
):
    """
    Setup AgentOps observability.
    
    AgentOps provides session replays, metrics, and monitoring for ADK agents.
    With just two lines of code, get comprehensive observability.
    
    Args:
        api_key: AgentOps API key. Falls back to AGENTOPS_API_KEY env var.
        trace_name: Name for your trace.
        auto_start_session: Whether to auto-start session.
    
    Example:
        import agentops
        agentops.init(api_key="...", trace_name="my-trace")
    """
    try:
        import agentops
        
        agentops.init(
            api_key=api_key or os.getenv("AGENTOPS_API_KEY"),
            trace_name=trace_name,
            auto_start_session=auto_start_session,
        )
        return True
    except ImportError:
        print("AgentOps not installed. Run: pip install agentops")
        return False


# =============================================================================
# Arize AX Integration
# =============================================================================

@dataclass
class ArizeAXConfig:
    """Configuration for Arize AX integration."""
    space_id: Optional[str] = None
    api_key: Optional[str] = None
    project_name: str = "adk-project"
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("ARIZE_API_KEY")


arize_ax_config = ArizeAXConfig()


def setup_arize_ax(
    space_id: Optional[str] = None,
    api_key: Optional[str] = None,
    project_name: str = "adk-project",
):
    """
    Setup Arize AX observability.
    
    Arize AX provides production-grade observability for monitoring,
    debugging, and improving LLM applications at scale.
    
    Args:
        space_id: Arize space ID from app settings.
        api_key: Arize API key.
        project_name: Project name in Arize.
    
    Example:
        from arize.otel import register
        from openinference.instrumentation.google_adk import GoogleADKInstrumentor
        
        tracer_provider = register(space_id="...", api_key="...", project_name="...")
        GoogleADKInstrumentor().instrument(tracer_provider=tracer_provider)
    """
    try:
        from arize.otel import register
        from openinference.instrumentation.google_adk import GoogleADKInstrumentor
        
        tracer_provider = register(
            space_id=space_id,
            api_key=api_key or os.getenv("ARIZE_API_KEY"),
            project_name=project_name,
        )
        GoogleADKInstrumentor().instrument(tracer_provider=tracer_provider)
        return tracer_provider
    except ImportError:
        print("Arize packages not installed. Run: pip install openinference-instrumentation-google-adk arize-otel")
        return None


# =============================================================================
# Phoenix Integration
# =============================================================================

@dataclass
class PhoenixConfig:
    """Configuration for Phoenix integration."""
    api_key: Optional[str] = None
    collector_endpoint: Optional[str] = None
    project_name: str = "adk-project"
    auto_instrument: bool = True
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("PHOENIX_API_KEY")
        self.collector_endpoint = self.collector_endpoint or os.getenv("PHOENIX_COLLECTOR_ENDPOINT")


phoenix_config = PhoenixConfig()


def setup_phoenix(
    project_name: str = "adk-project",
    auto_instrument: bool = True,
):
    """
    Setup Phoenix observability.
    
    Phoenix is an open-source, self-hosted observability platform.
    
    Args:
        project_name: Project name for traces.
        auto_instrument: Auto-instrument based on installed dependencies.
    
    Example:
        from phoenix.otel import register
        tracer_provider = register(project_name="my-app", auto_instrument=True)
    """
    try:
        from phoenix.otel import register
        
        tracer_provider = register(
            project_name=project_name,
            auto_instrument=auto_instrument,
        )
        return tracer_provider
    except ImportError:
        print("Phoenix not installed. Run: pip install arize-phoenix-otel openinference-instrumentation-google-adk")
        return None


# =============================================================================
# MLflow Integration
# =============================================================================

@dataclass
class MLflowConfig:
    """Configuration for MLflow integration."""
    tracking_uri: str = "http://localhost:5000"
    experiment_id: Optional[str] = None
    
    def __post_init__(self):
        self.experiment_id = self.experiment_id or os.getenv("MLFLOW_EXPERIMENT_ID")


mlflow_config = MLflowConfig()


def setup_mlflow(
    tracking_uri: str = "http://localhost:5000",
    experiment_id: Optional[str] = None,
):
    """
    Setup MLflow observability.
    
    MLflow Tracing provides first-class support for ingesting OpenTelemetry traces.
    
    Args:
        tracking_uri: MLflow tracking server URI.
        experiment_id: MLflow experiment ID.
    
    Example:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        exporter = OTLPSpanExporter(
            endpoint="http://localhost:5000/v1/traces",
            headers={"x-mlflow-experiment-id": "123"}
        )
    """
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        
        headers = {}
        if experiment_id:
            headers["x-mlflow-experiment-id"] = experiment_id
        
        exporter = OTLPSpanExporter(
            endpoint=f"{tracking_uri}/v1/traces",
            headers=headers,
        )
        
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        
        return provider
    except ImportError:
        print("MLflow packages not installed. Run: pip install mlflow>=3.6.0 opentelemetry-sdk opentelemetry-exporter-otlp-proto-http")
        return None


# =============================================================================
# Monocle Integration
# =============================================================================

@dataclass
class MonocleConfig:
    """Configuration for Monocle integration."""
    workflow_name: str = "adk-app"
    exporter: str = "file"  # "file" or "console"
    
    def __post_init__(self):
        self.exporter = os.getenv("MONOCLE_EXPORTER", self.exporter)


monocle_config = MonocleConfig()


def setup_monocle(workflow_name: str = "adk-app"):
    """
    Setup Monocle observability.
    
    Monocle is an open-source observability platform with automatic instrumentation.
    
    Args:
        workflow_name: Name for the workflow traces.
    
    Example:
        from monocle_apptrace import setup_monocle_telemetry
        setup_monocle_telemetry(workflow_name="my-adk-app")
    """
    try:
        from monocle_apptrace import setup_monocle_telemetry
        
        setup_monocle_telemetry(workflow_name=workflow_name)
        return True
    except ImportError:
        print("Monocle not installed. Run: pip install monocle_apptrace")
        return False


# =============================================================================
# Cloud Trace Integration
# =============================================================================

@dataclass
class CloudTraceConfig:
    """Configuration for Google Cloud Trace integration."""
    project_id: Optional[str] = None
    
    def __post_init__(self):
        self.project_id = self.project_id or os.getenv("GOOGLE_CLOUD_PROJECT")


cloud_trace_config = CloudTraceConfig()


def setup_cloud_trace(project_id: Optional[str] = None):
    """
    Setup Google Cloud Trace observability.
    
    Cloud Trace provides monitoring, debugging, and tracing for cloud deployments.
    
    Args:
        project_id: Google Cloud project ID.
    
    Example:
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        processor = export.BatchSpanProcessor(CloudTraceSpanExporter(project_id="..."))
    """
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace import export
        
        provider = TracerProvider()
        processor = export.BatchSpanProcessor(
            CloudTraceSpanExporter(project_id=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        return provider
    except ImportError:
        print("Cloud Trace packages not installed. Run: pip install opentelemetry-exporter-cloud-trace")
        return None


# =============================================================================
# W&B Weave Integration
# =============================================================================

@dataclass
class WeaveConfig:
    """Configuration for W&B Weave integration."""
    wandb_api_key: Optional[str] = None
    project_id: str = "entity/project"
    base_url: str = "https://trace.wandb.ai"
    
    def __post_init__(self):
        self.wandb_api_key = self.wandb_api_key or os.getenv("WANDB_API_KEY")


weave_config = WeaveConfig()


def setup_weave(
    project_id: str = "entity/project",
    wandb_api_key: Optional[str] = None,
):
    """
    Setup W&B Weave observability.
    
    Weave provides logging and visualization of model calls.
    
    Args:
        project_id: W&B project ID (entity/project format).
        wandb_api_key: W&B API key.
    
    Example:
        import base64
        AUTH = base64.b64encode(f"api:{WANDB_API_KEY}".encode()).decode()
        exporter = OTLPSpanExporter(endpoint="...", headers={"Authorization": f"Basic {AUTH}"})
    """
    try:
        import base64
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        
        api_key = wandb_api_key or os.getenv("WANDB_API_KEY")
        auth = base64.b64encode(f"api:{api_key}".encode()).decode()
        
        exporter = OTLPSpanExporter(
            endpoint=f"https://trace.wandb.ai/otel/v1/traces",
            headers={
                "Authorization": f"Basic {auth}",
                "project_id": project_id,
            },
        )
        
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        
        return provider
    except ImportError:
        print("Weave packages not installed. Run: pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http")
        return None


# =============================================================================
# Freeplay Integration
# =============================================================================

@dataclass
class FreeplayConfig:
    """Configuration for Freeplay integration."""
    api_key: Optional[str] = None
    project_id: Optional[str] = None
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("FREEPLAY_API_KEY")


freeplay_config = FreeplayConfig()


def setup_freeplay(
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
):
    """
    Setup Freeplay testing and evaluation.
    
    Freeplay provides testing and evaluation capabilities for AI agents.
    
    Args:
        api_key: Freeplay API key.
        project_id: Freeplay project ID.
    """
    # Freeplay setup would go here
    # This is a placeholder for the integration
    return {
        "api_key": api_key or os.getenv("FREEPLAY_API_KEY"),
        "project_id": project_id,
    }
