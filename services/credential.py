"""
Credential service setup for Google ADK.

Provides functions for creating and configuring credential services
that handle authentication for tools and APIs.

Note: The credential service is typically configured at the Runner level
and handles OAuth flows, API key management, and token refresh.
"""

from typing import Optional, Any

from config.settings import get_settings


def create_credential_service(
    service_type: str = "default",
    **kwargs
) -> Optional[Any]:
    """
    Create a credential service for handling tool authentication.
    
    The credential service manages authentication credentials for tools
    that require OAuth, API keys, or other authentication mechanisms.
    
    Args:
        service_type: The type of credential service to create.
                     Currently only "default" is supported.
        **kwargs: Additional configuration options.
    
    Returns:
        Optional[Any]: The credential service instance, or None if not configured.
    
    Note:
        Credential services are typically optional and used for advanced
        authentication scenarios. For simple OAuth flows, the tools handle
        authentication directly with auth_scheme and auth_credential.
    
    Example:
        # For most use cases, credential_service can be None
        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            credential_service=None  # Tools handle their own auth
        )
        
        # For centralized credential management
        credential_service = create_credential_service()
        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            credential_service=credential_service
        )
    """
    # For now, return None as most authentication is handled
    # at the tool level with auth_scheme and auth_credential
    # 
    # In a production system, you might implement:
    # - A custom BaseCredentialService subclass
    # - Integration with a secrets manager
    # - OAuth token refresh logic
    return None


def get_oauth_credentials():
    """
    Get OAuth credentials from settings.
    
    Returns:
        tuple: (client_id, client_secret) from settings.
    
    Example:
        client_id, client_secret = get_oauth_credentials()
        gmail_toolset = GmailToolset(
            client_id=client_id,
            client_secret=client_secret
        )
    """
    settings = get_settings()
    return (
        settings.oauth.client_id,
        settings.oauth.client_secret
    )


def get_service_account_path() -> Optional[str]:
    """
    Get the service account credentials file path.
    
    Returns:
        Optional[str]: Path to service account JSON, or None.
    
    Example:
        sa_path = get_service_account_path()
        if sa_path:
            # Use service account for authentication
            toolset = BigQueryToolset(service_account=sa_path)
    """
    import os
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
