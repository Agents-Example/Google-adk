"""
App configuration for Google ADK Multi-Agent System.

The App class provides a high-level interface for configuring and
running agents with web-based UI support.

Demonstrates:
- App configuration with all options
- ResumabilityConfig for session persistence
- Context cache configuration
- Web interface setup
"""

from typing import Optional, List

from google.adk import App
from google.adk.app import ResumabilityConfig, ContextCacheConfig
from google.adk.agents import LlmAgent
from google.adk.sessions import BaseSessionService
from google.adk.artifacts import BaseArtifactService
from google.adk.memory import BaseMemoryService

from config.settings import get_settings
from services.session import create_session_service
from services.artifact import create_artifact_service
from services.memory import create_memory_service
from agents.orchestrator.agent import build_multi_agent_system


def create_app(
    agent: Optional[LlmAgent] = None,
    session_service: Optional[BaseSessionService] = None,
    artifact_service: Optional[BaseArtifactService] = None,
    memory_service: Optional[BaseMemoryService] = None,
    enable_resumability: bool = True,
    enable_context_cache: bool = False,
) -> App:
    """
    Create a configured App instance.
    
    The App provides a web-based interface for interacting with agents.
    It handles session management, artifact storage, and memory.
    
    Args:
        agent: The root agent to use. Defaults to full multi-agent system.
        session_service: Session service. Defaults to InMemory.
        artifact_service: Artifact service. Defaults to InMemory.
        memory_service: Memory service. Defaults to InMemory.
        enable_resumability: Enable session resumption.
        enable_context_cache: Enable context caching.
    
    Returns:
        App: A configured App instance.
    
    Example:
        app = create_app()
        app.run()  # Start web interface
    """
    settings = get_settings()
    
    # Create default services if not provided
    if session_service is None:
        session_service = create_session_service()
    
    if artifact_service is None:
        artifact_service = create_artifact_service("inmemory")
    
    if memory_service is None:
        memory_service = create_memory_service("inmemory")
    
    # Create default agent if not provided
    if agent is None:
        agent = build_multi_agent_system()
    
    # Configure resumability
    resumability_config = None
    if enable_resumability:
        resumability_config = ResumabilityConfig(
            enabled=True,
            # Additional resumability options can be configured here
        )
    
    # Configure context cache
    context_cache_config = None
    if enable_context_cache:
        context_cache_config = ContextCacheConfig(
            enabled=True,
            # Additional cache options can be configured here
        )
    
    return App(
        agent=agent,
        session_service=session_service,
        artifact_service=artifact_service,
        memory_service=memory_service,
        resumability_config=resumability_config,
        context_cache_config=context_cache_config,
    )


def create_minimal_app(agent: LlmAgent) -> App:
    """
    Create a minimal App with defaults.
    
    Uses all default services for quick development setup.
    
    Args:
        agent: The agent to use.
    
    Returns:
        App: A minimal App instance.
    """
    return App(agent=agent)


def create_production_app(
    agent: LlmAgent,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> App:
    """
    Create a production-ready App with Vertex AI services.
    
    Uses Vertex AI backend services for production deployment.
    
    Args:
        agent: The agent to use.
        project: GCP project ID.
        location: GCP location.
    
    Returns:
        App: A production-ready App instance.
    """
    settings = get_settings()
    
    # Use Vertex AI services
    from services.session import create_vertex_session_service
    from services.artifact import create_gcs_artifact_service
    from services.memory import create_vertex_memory_bank_service
    
    return App(
        agent=agent,
        session_service=create_vertex_session_service(
            project=project or settings.google_ai.project,
            location=location or settings.google_ai.location,
        ),
        artifact_service=create_gcs_artifact_service(
            bucket_name=settings.artifacts.gcs_bucket,
        ),
        memory_service=create_vertex_memory_bank_service(
            project=project or settings.google_ai.project,
            location=location or settings.google_ai.location,
        ),
        resumability_config=ResumabilityConfig(enabled=True),
    )


# Pre-configured App instances

# Development app with InMemory services
settings = get_settings()

# Inline configuration style
dev_app = App(
    agent=build_multi_agent_system(),
    session_service=create_session_service(use_vertex=False),
    artifact_service=create_artifact_service("inmemory"),
    memory_service=create_memory_service("inmemory"),
)


"""
App Usage Patterns
==================

1. Development Mode
-------------------
from app import create_app

app = create_app()
app.run(host="localhost", port=8080)

2. Production Mode
------------------
from app import create_production_app
from agents import build_multi_agent_system

agent = build_multi_agent_system()
app = create_production_app(
    agent=agent,
    project="my-gcp-project",
    location="us-central1"
)
app.run()

3. Custom Configuration
-----------------------
from google.adk import App
from google.adk.app import ResumabilityConfig

app = App(
    agent=my_agent,
    session_service=my_session_service,
    artifact_service=my_artifact_service,
    memory_service=my_memory_service,
    resumability_config=ResumabilityConfig(enabled=True),
)

4. Minimal Setup
----------------
from google.adk import App

app = App(agent=my_agent)
app.run()

App Features:
- Web-based chat interface
- Session management
- File upload/download (artifacts)
- Memory search
- OAuth flow handling
- Streaming responses
"""
