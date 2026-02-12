"""
Environment-based settings for the Google ADK Multi-Agent System.

Demonstrates loading configuration from environment variables with defaults.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class GoogleAISettings:
    """Settings for Google AI / Vertex AI."""
    
    use_vertex_ai: bool = field(
        default_factory=lambda: os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
    )
    api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY")
    )
    project: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location: str = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )


@dataclass
class ModelSettings:
    """Settings for LLM models."""
    
    default_model: str = field(
        default_factory=lambda: os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    )
    thinking_model: str = field(
        default_factory=lambda: os.getenv("THINKING_MODEL", "gemini-2.5-pro")
    )


@dataclass
class OAuthSettings:
    """OAuth2 settings for Google API toolsets."""
    
    client_id: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    )
    client_secret: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    )


@dataclass
class VertexSearchSettings:
    """Vertex AI Search settings."""
    
    data_store_id: Optional[str] = field(
        default_factory=lambda: os.getenv("VERTEX_AI_SEARCH_DATA_STORE_ID")
    )
    engine_id: Optional[str] = field(
        default_factory=lambda: os.getenv("VERTEX_AI_SEARCH_ENGINE_ID")
    )


@dataclass
class BigQuerySettings:
    """BigQuery settings."""
    
    project: Optional[str] = field(
        default_factory=lambda: os.getenv("BIGQUERY_PROJECT")
    )
    dataset: Optional[str] = field(
        default_factory=lambda: os.getenv("BIGQUERY_DATASET")
    )


@dataclass
class APIHubSettings:
    """API Hub settings."""
    
    resource_name: Optional[str] = field(
        default_factory=lambda: os.getenv("APIHUB_RESOURCE_NAME")
    )


@dataclass
class AppIntegrationSettings:
    """Application Integration settings."""
    
    project: Optional[str] = field(
        default_factory=lambda: os.getenv("APP_INTEGRATION_PROJECT")
    )
    location: str = field(
        default_factory=lambda: os.getenv("APP_INTEGRATION_LOCATION", "us-central1")
    )
    integration_name: Optional[str] = field(
        default_factory=lambda: os.getenv("APP_INTEGRATION_NAME")
    )


@dataclass
class MCPSettings:
    """MCP Server settings."""
    
    # Stdio settings
    stdio_command: str = field(
        default_factory=lambda: os.getenv("MCP_STDIO_COMMAND", "npx")
    )
    stdio_args: list = field(
        default_factory=lambda: os.getenv("MCP_STDIO_ARGS", "-y,@modelcontextprotocol/server-filesystem").split(",")
    )
    
    # SSE settings
    sse_url: Optional[str] = field(
        default_factory=lambda: os.getenv("MCP_SSE_URL")
    )
    
    # HTTP settings
    http_url: Optional[str] = field(
        default_factory=lambda: os.getenv("MCP_HTTP_URL")
    )


@dataclass
class ToolboxSettings:
    """Toolbox settings."""
    
    server_url: str = field(
        default_factory=lambda: os.getenv("TOOLBOX_SERVER_URL", "http://127.0.0.1:5000")
    )


@dataclass
class MemorySettings:
    """Memory service settings."""
    
    memory_bank_agent_engine_id: Optional[str] = field(
        default_factory=lambda: os.getenv("MEMORY_BANK_AGENT_ENGINE_ID")
    )
    rag_corpus_name: Optional[str] = field(
        default_factory=lambda: os.getenv("RAG_CORPUS_NAME")
    )


@dataclass
class ArtifactSettings:
    """Artifact storage settings."""
    
    gcs_bucket: Optional[str] = field(
        default_factory=lambda: os.getenv("GCS_ARTIFACT_BUCKET")
    )
    file_root: str = field(
        default_factory=lambda: os.getenv("FILE_ARTIFACT_ROOT", "/tmp/adk_artifacts")
    )


@dataclass
class SessionSettings:
    """Session service settings."""
    
    agent_engine_id: Optional[str] = field(
        default_factory=lambda: os.getenv("SESSION_AGENT_ENGINE_ID")
    )


@dataclass
class DebugSettings:
    """Debug and logging settings."""
    
    output_path: str = field(
        default_factory=lambda: os.getenv("DEBUG_OUTPUT_PATH", "adk_debug.yaml")
    )
    enable_debug_logging: bool = field(
        default_factory=lambda: os.getenv("ENABLE_DEBUG_LOGGING", "false").lower() == "true"
    )


@dataclass
class RuntimeSettings:
    """Runtime configuration settings."""
    
    max_llm_calls: int = field(
        default_factory=lambda: int(os.getenv("MAX_LLM_CALLS", "500"))
    )
    streaming_mode: str = field(
        default_factory=lambda: os.getenv("STREAMING_MODE", "NONE")
    )


@dataclass
class Settings:
    """
    Main settings container aggregating all configuration sections.
    
    Usage:
        settings = get_settings()
        model = settings.models.default_model
        project = settings.google_ai.project
    """
    
    google_ai: GoogleAISettings = field(default_factory=GoogleAISettings)
    models: ModelSettings = field(default_factory=ModelSettings)
    oauth: OAuthSettings = field(default_factory=OAuthSettings)
    vertex_search: VertexSearchSettings = field(default_factory=VertexSearchSettings)
    bigquery: BigQuerySettings = field(default_factory=BigQuerySettings)
    api_hub: APIHubSettings = field(default_factory=APIHubSettings)
    app_integration: AppIntegrationSettings = field(default_factory=AppIntegrationSettings)
    mcp: MCPSettings = field(default_factory=MCPSettings)
    toolbox: ToolboxSettings = field(default_factory=ToolboxSettings)
    memory: MemorySettings = field(default_factory=MemorySettings)
    artifacts: ArtifactSettings = field(default_factory=ArtifactSettings)
    sessions: SessionSettings = field(default_factory=SessionSettings)
    debug: DebugSettings = field(default_factory=DebugSettings)
    runtime: RuntimeSettings = field(default_factory=RuntimeSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get the singleton Settings instance.
    
    Returns:
        Settings: The application settings.
    """
    return Settings()
