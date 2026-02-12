"""
Memory service factories for Google ADK.

Provides factory functions for creating memory services:
- InMemoryMemoryService: For development (keyword matching)
- VertexAiMemoryBankService: For Vertex AI Memory Bank (semantic search)
- VertexAiRagMemoryService: For Vertex AI RAG (retrieval-augmented generation)

Memory services enable agents to:
- Store and retrieve session memories
- Search memories semantically
- Provide context from past interactions
"""

from typing import Optional

from google.adk.memory import (
    BaseMemoryService,
    InMemoryMemoryService,
    VertexAiMemoryBankService,
    VertexAiRagMemoryService,
)

from config.settings import get_settings


def create_inmemory_memory_service() -> InMemoryMemoryService:
    """
    Create an in-memory memory service for development.
    
    The InMemoryMemoryService uses simple keyword matching instead of
    semantic search. It's suitable for testing and prototyping but
    not for production use.
    
    Returns:
        InMemoryMemoryService: An in-memory memory service instance.
    
    Example:
        memory_service = create_inmemory_memory_service()
        await memory_service.add_session_to_memory(session)
        results = await memory_service.search_memory(
            app_name="my_app",
            user_id="user123",
            query="previous conversations about Python"
        )
    """
    return InMemoryMemoryService()


def create_vertex_memory_bank_service(
    project: Optional[str] = None,
    location: Optional[str] = None,
    agent_engine_id: Optional[str] = None,
) -> VertexAiMemoryBankService:
    """
    Create a Vertex AI Memory Bank service.
    
    The VertexAiMemoryBankService provides semantic search over
    conversation memories using Vertex AI's memory bank feature.
    
    Args:
        project: GCP project ID. Defaults to settings.
        location: GCP location. Defaults to settings.
        agent_engine_id: The Agent Engine resource ID for the memory bank.
    
    Returns:
        VertexAiMemoryBankService: A Vertex AI memory bank service instance.
    
    Example:
        memory_service = create_vertex_memory_bank_service(
            project="my-project",
            agent_engine_id="12345"
        )
    """
    settings = get_settings()
    
    return VertexAiMemoryBankService(
        project=project or settings.google_ai.project,
        location=location or settings.google_ai.location,
        agent_engine_id=agent_engine_id or settings.memory.memory_bank_agent_engine_id,
    )


def create_vertex_rag_memory_service(
    rag_corpus: Optional[str] = None,
    similarity_top_k: Optional[int] = None,
    vector_distance_threshold: float = 10.0,
) -> VertexAiRagMemoryService:
    """
    Create a Vertex AI RAG memory service.
    
    The VertexAiRagMemoryService uses Vertex AI RAG for storage and
    retrieval of memories. Provides semantic search with configurable
    similarity parameters.
    
    Args:
        rag_corpus: The Vertex AI RAG corpus resource name.
        similarity_top_k: Number of contexts to retrieve.
        vector_distance_threshold: Maximum distance for results.
    
    Returns:
        VertexAiRagMemoryService: A Vertex AI RAG memory service instance.
    
    Example:
        memory_service = create_vertex_rag_memory_service(
            rag_corpus="projects/my-project/locations/us-central1/ragCorpora/123",
            similarity_top_k=10
        )
    """
    settings = get_settings()
    
    return VertexAiRagMemoryService(
        rag_corpus=rag_corpus or settings.memory.rag_corpus_name,
        similarity_top_k=similarity_top_k,
        vector_distance_threshold=vector_distance_threshold,
    )


def create_memory_service(
    service_type: str = "inmemory",
    **kwargs
) -> BaseMemoryService:
    """
    Factory function to create the appropriate memory service.
    
    Args:
        service_type: One of "inmemory", "memory_bank", or "rag".
        **kwargs: Additional arguments passed to the service constructor.
    
    Returns:
        BaseMemoryService: The created memory service.
    
    Example:
        # In-memory for development
        memory_service = create_memory_service("inmemory")
        
        # Vertex AI Memory Bank for production
        memory_service = create_memory_service(
            "memory_bank",
            agent_engine_id="12345"
        )
        
        # Vertex AI RAG for RAG-based memory
        memory_service = create_memory_service(
            "rag",
            rag_corpus="projects/my-project/..."
        )
    """
    if service_type == "inmemory":
        return create_inmemory_memory_service()
    elif service_type == "memory_bank":
        return create_vertex_memory_bank_service(**kwargs)
    elif service_type == "rag":
        return create_vertex_rag_memory_service(**kwargs)
    else:
        raise ValueError(
            f"Unknown memory service type: {service_type}. "
            "Must be one of: inmemory, memory_bank, rag"
        )
