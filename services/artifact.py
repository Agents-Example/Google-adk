"""
Artifact service factories for Google ADK.

Provides factory functions for creating artifact services:
- InMemoryArtifactService: For development and testing
- FileArtifactService: For file-based storage
- GcsArtifactService: For Google Cloud Storage

Artifact services manage file-like artifacts including:
- Saving and loading artifacts
- Versioning artifacts
- Listing artifacts
"""

from typing import Optional

from google.adk.artifacts import (
    BaseArtifactService,
    InMemoryArtifactService,
    FileArtifactService,
    GcsArtifactService,
)

from config.settings import get_settings


def create_inmemory_artifact_service() -> InMemoryArtifactService:
    """
    Create an in-memory artifact service for development.
    
    The InMemoryArtifactService stores all artifacts in memory.
    It's suitable for testing but data is lost when the process ends.
    
    Returns:
        InMemoryArtifactService: An in-memory artifact service instance.
    
    Example:
        artifact_service = create_inmemory_artifact_service()
        version = await artifact_service.save_artifact(
            app_name="my_app",
            user_id="user123",
            filename="report.pdf",
            artifact=pdf_part
        )
    """
    return InMemoryArtifactService()


def create_file_artifact_service(
    root_dir: Optional[str] = None,
) -> FileArtifactService:
    """
    Create a file-based artifact service.
    
    The FileArtifactService stores artifacts on the local filesystem.
    Supports versioning and nested filenames.
    
    Args:
        root_dir: Root directory for artifact storage.
                 Defaults to settings.artifacts.file_root.
    
    Returns:
        FileArtifactService: A file-based artifact service instance.
    
    Example:
        artifact_service = create_file_artifact_service(
            root_dir="/data/artifacts"
        )
    """
    settings = get_settings()
    
    return FileArtifactService(
        root_dir=root_dir or settings.artifacts.file_root
    )


def create_gcs_artifact_service(
    bucket_name: Optional[str] = None,
    **kwargs
) -> GcsArtifactService:
    """
    Create a Google Cloud Storage artifact service.
    
    The GcsArtifactService stores artifacts in a GCS bucket.
    Suitable for production deployments with cloud storage.
    
    Args:
        bucket_name: GCS bucket name. Defaults to settings.
        **kwargs: Additional arguments for the GCS client.
    
    Returns:
        GcsArtifactService: A GCS artifact service instance.
    
    Example:
        artifact_service = create_gcs_artifact_service(
            bucket_name="my-artifact-bucket"
        )
    """
    settings = get_settings()
    
    return GcsArtifactService(
        bucket_name=bucket_name or settings.artifacts.gcs_bucket,
        **kwargs
    )


def create_artifact_service(
    service_type: str = "inmemory",
    **kwargs
) -> BaseArtifactService:
    """
    Factory function to create the appropriate artifact service.
    
    Args:
        service_type: One of "inmemory", "file", or "gcs".
        **kwargs: Additional arguments passed to the service constructor.
    
    Returns:
        BaseArtifactService: The created artifact service.
    
    Example:
        # In-memory for development
        artifact_service = create_artifact_service("inmemory")
        
        # File-based for local persistence
        artifact_service = create_artifact_service(
            "file",
            root_dir="/data/artifacts"
        )
        
        # GCS for production
        artifact_service = create_artifact_service(
            "gcs",
            bucket_name="my-bucket"
        )
    """
    if service_type == "inmemory":
        return create_inmemory_artifact_service()
    elif service_type == "file":
        return create_file_artifact_service(**kwargs)
    elif service_type == "gcs":
        return create_gcs_artifact_service(**kwargs)
    else:
        raise ValueError(
            f"Unknown artifact service type: {service_type}. "
            "Must be one of: inmemory, file, gcs"
        )
