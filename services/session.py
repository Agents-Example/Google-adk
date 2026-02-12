"""
Session service factories for Google ADK.

Provides factory functions for creating session services:
- InMemorySessionService: For development and testing
- VertexAiSessionService: For production with Vertex AI Agent Engine

Session services manage conversation sessions including:
- Creating and retrieving sessions
- Appending events to sessions
- Managing session state
"""

from typing import Optional

from google.adk.sessions import (
    BaseSessionService,
    InMemorySessionService,
    VertexAiSessionService,
)

from config.settings import get_settings


def create_inmemory_session_service() -> InMemorySessionService:
    """
    Create an in-memory session service for development.
    
    The InMemorySessionService stores all session data in memory.
    It's suitable for testing and development but not for production
    as data is lost when the process ends.
    
    Returns:
        InMemorySessionService: An in-memory session service instance.
    
    Example:
        session_service = create_inmemory_session_service()
        session = await session_service.create_session(
            app_name="my_app",
            user_id="user123"
        )
    """
    return InMemorySessionService()


def create_vertex_session_service(
    project: Optional[str] = None,
    location: Optional[str] = None,
    agent_engine_id: Optional[str] = None,
) -> VertexAiSessionService:
    """
    Create a Vertex AI session service for production.
    
    The VertexAiSessionService connects to Vertex AI Agent Engine
    for persistent session storage and management.
    
    Args:
        project: GCP project ID. Defaults to settings.
        location: GCP location. Defaults to settings.
        agent_engine_id: The Agent Engine resource ID. Defaults to settings.
    
    Returns:
        VertexAiSessionService: A Vertex AI session service instance.
    
    Example:
        session_service = create_vertex_session_service(
            project="my-project",
            location="us-central1",
            agent_engine_id="12345"
        )
    """
    settings = get_settings()
    
    return VertexAiSessionService(
        project=project or settings.google_ai.project,
        location=location or settings.google_ai.location,
        agent_engine_id=agent_engine_id or settings.sessions.agent_engine_id,
    )


def create_session_service(
    use_vertex: Optional[bool] = None,
    **kwargs
) -> BaseSessionService:
    """
    Factory function to create the appropriate session service.
    
    Automatically selects between InMemory and Vertex AI based on
    configuration or explicit parameter.
    
    Args:
        use_vertex: If True, use Vertex AI. If False, use InMemory.
                   If None, uses the GOOGLE_GENAI_USE_VERTEXAI setting.
        **kwargs: Additional arguments passed to the service constructor.
    
    Returns:
        BaseSessionService: The created session service.
    
    Example:
        # Auto-select based on environment
        session_service = create_session_service()
        
        # Force in-memory
        session_service = create_session_service(use_vertex=False)
        
        # Force Vertex AI with custom config
        session_service = create_session_service(
            use_vertex=True,
            project="custom-project"
        )
    """
    settings = get_settings()
    
    if use_vertex is None:
        use_vertex = settings.google_ai.use_vertex_ai
    
    if use_vertex:
        return create_vertex_session_service(**kwargs)
    else:
        return create_inmemory_session_service()
