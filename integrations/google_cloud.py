"""
Google Cloud integrations for Google ADK.

Provides configurations for Google Cloud services:
- Vertex AI Express Mode (free tier)
- Vertex AI RAG Engine
- Cloud PubSub
"""

import os
from typing import Optional
from dataclasses import dataclass


# =============================================================================
# Vertex AI Express Mode
# =============================================================================

@dataclass
class ExpressModeConfig:
    """
    Configuration for Vertex AI Express Mode.
    
    Express Mode provides no-cost access for prototyping:
    - VertexAiSessionService
    - VertexAiMemoryBankService
    
    Limitations:
    - Projects valid for 90 days
    - Limited quota (10 Agent Engines max)
    - Rate limits on session/memory operations
    """
    api_key: Optional[str] = None
    agent_engine_id: Optional[str] = None
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("GOOGLE_API_KEY")


express_mode_config = ExpressModeConfig()


def setup_express_mode(
    api_key: Optional[str] = None,
    display_name: str = "Demo Agent Engine",
    description: str = "Agent Engine for Session and Memory",
):
    """
    Setup Vertex AI Express Mode.
    
    Express Mode provides free access to Vertex AI services for development.
    
    Args:
        api_key: Vertex AI Express Mode API key.
        display_name: Agent Engine display name.
        description: Agent Engine description.
    
    Returns:
        tuple: (agent_engine, app_id)
    
    Example:
        # Set environment variables
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
        os.environ["GOOGLE_API_KEY"] = "your-express-mode-key"
        
        # Create Agent Engine
        engine, app_id = setup_express_mode(api_key="...")
        
        # Use with services
        session_service = VertexAiSessionService(agent_engine_id=app_id)
        memory_service = VertexAiMemoryBankService(agent_engine_id=app_id)
    """
    try:
        import vertexai
        from vertexai import agent_engines
        
        client = vertexai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        
        agent_engine = client.agent_engines.create(
            config={
                "display_name": display_name,
                "description": description,
            }
        )
        
        app_id = agent_engine.api_resource.name.split('/')[-1]
        
        return agent_engine, app_id
    except ImportError:
        print("Vertex AI not installed. Run: pip install google-adk[vertexai]")
        return None, None


# =============================================================================
# Vertex AI RAG Engine
# =============================================================================

@dataclass
class VertexRAGConfig:
    """
    Configuration for Vertex AI RAG Engine.
    
    RAG Engine provides retrieval-augmented generation capabilities.
    """
    project: Optional[str] = None
    location: str = "us-central1"
    corpus_name: Optional[str] = None
    similarity_top_k: int = 10
    vector_distance_threshold: float = 10.0
    
    def __post_init__(self):
        self.project = self.project or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.corpus_name = self.corpus_name or os.getenv("RAG_CORPUS_NAME")


def get_vertex_rag_config(
    project: Optional[str] = None,
    location: str = "us-central1",
    corpus_name: Optional[str] = None,
    similarity_top_k: int = 10,
) -> VertexRAGConfig:
    """
    Get Vertex AI RAG Engine configuration.
    
    Args:
        project: GCP project ID.
        location: GCP location.
        corpus_name: RAG corpus resource name.
        similarity_top_k: Number of results to retrieve.
    
    Returns:
        VertexRAGConfig: Configuration object.
    
    Usage with ADK Memory Service:
        from google.adk.memory import VertexAiRagMemoryService
        
        config = get_vertex_rag_config()
        memory_service = VertexAiRagMemoryService(
            rag_corpus=config.corpus_name,
            similarity_top_k=config.similarity_top_k,
        )
    """
    return VertexRAGConfig(
        project=project,
        location=location,
        corpus_name=corpus_name,
        similarity_top_k=similarity_top_k,
    )


# =============================================================================
# Cloud PubSub
# =============================================================================

@dataclass
class PubSubConfig:
    """Configuration for Google Cloud PubSub."""
    project: Optional[str] = None
    topic: Optional[str] = None
    subscription: Optional[str] = None
    
    def __post_init__(self):
        self.project = self.project or os.getenv("GOOGLE_CLOUD_PROJECT")


def get_pubsub_config(
    project: Optional[str] = None,
    topic: Optional[str] = None,
    subscription: Optional[str] = None,
) -> PubSubConfig:
    """
    Get PubSub configuration for event-driven agents.
    
    Args:
        project: GCP project ID.
        topic: PubSub topic name.
        subscription: PubSub subscription name.
    
    Returns:
        PubSubConfig: Configuration object.
    """
    return PubSubConfig(
        project=project,
        topic=topic,
        subscription=subscription,
    )


# =============================================================================
# Pub/Sub Toolset (publish_message, pull_messages, acknowledge_messages)
# =============================================================================

def get_pubsub_toolset(project: Optional[str] = None):
    """
    Get Google Cloud Pub/Sub toolset for agents.
    Requires google-adk with PubSubToolset (Python v1.22.0+).
    """
    try:
        from google.adk.tools import PubSubToolset
        return PubSubToolset(project_id=project or os.getenv("GOOGLE_CLOUD_PROJECT"))
    except ImportError:
        return None


# =============================================================================
# Bigtable Toolset (list_instances, get_instance_info, list_tables, get_table_info, execute_sql)
# =============================================================================

def get_bigtable_toolset(project: Optional[str] = None, instance: Optional[str] = None):
    """
    Get Google Cloud Bigtable toolset for agents.
    Requires google-adk with BigtableToolset (Python v1.12.0+).
    """
    try:
        from google.adk.tools import BigtableToolset
        kwargs = {"project_id": project or os.getenv("GOOGLE_CLOUD_PROJECT")}
        if instance:
            kwargs["instance_id"] = instance
        return BigtableToolset(**kwargs)
    except ImportError:
        return None


# =============================================================================
# Spanner Toolset (list_table_names, get_table_schema, execute_sql, similarity_search, etc.)
# =============================================================================

def get_spanner_toolset(
    project: Optional[str] = None,
    instance: Optional[str] = None,
    database: Optional[str] = None,
):
    """
    Get Google Cloud Spanner toolset for agents.
    Requires google-adk with SpannerToolset (Python v1.11.0+).
    """
    try:
        from google.adk.tools import SpannerToolset
        kwargs = {"project_id": project or os.getenv("GOOGLE_CLOUD_PROJECT")}
        if instance:
            kwargs["instance_id"] = instance
        if database:
            kwargs["database_id"] = database
        return SpannerToolset(**kwargs)
    except ImportError:
        return None
