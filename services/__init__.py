"""
Services module for Google ADK Multi-Agent System.

This module provides factory functions for creating various backend services:
- Session services (InMemory, VertexAI)
- Artifact services (InMemory, File, GCS)
- Memory services (InMemory, VertexAI Memory Bank, VertexAI RAG)
- Credential services
"""

from services.session import (
    create_session_service,
    create_inmemory_session_service,
    create_vertex_session_service,
)
from services.artifact import (
    create_artifact_service,
    create_inmemory_artifact_service,
    create_file_artifact_service,
    create_gcs_artifact_service,
)
from services.memory import (
    create_memory_service,
    create_inmemory_memory_service,
    create_vertex_memory_bank_service,
    create_vertex_rag_memory_service,
)
from services.credential import (
    create_credential_service,
)

__all__ = [
    # Session
    "create_session_service",
    "create_inmemory_session_service",
    "create_vertex_session_service",
    # Artifact
    "create_artifact_service",
    "create_inmemory_artifact_service",
    "create_file_artifact_service",
    "create_gcs_artifact_service",
    # Memory
    "create_memory_service",
    "create_inmemory_memory_service",
    "create_vertex_memory_bank_service",
    "create_vertex_rag_memory_service",
    # Credential
    "create_credential_service",
]
