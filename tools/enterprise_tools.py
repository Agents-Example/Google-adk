"""
Enterprise tools for Google ADK.

This module provides enterprise-grade tool integrations:
- APIHubToolset: Generate tools from API Hub resources
- ApplicationIntegrationToolset: Integration with Application Integration
- ToolboxToolset: MCP Toolbox SDK integration

These tools are designed for enterprise environments with
centralized API management and integration platforms.
"""

from typing import Optional, List, Dict, Any

from google.adk.tools import (
    APIHubToolset,
    ToolboxToolset,
)
from google.adk.tools.application_integration_tool import (
    ApplicationIntegrationToolset,
)
from google.adk.tools.base_toolset import BaseToolset, ToolPredicate
from google.adk.auth import AuthScheme, AuthCredential

from config.settings import get_settings


def get_apihub_toolset(
    apihub_resource_name: Optional[str] = None,
    access_token: Optional[str] = None,
    service_account_json: Optional[str] = None,
    name: str = "",
    description: str = "",
    lazy_load_spec: bool = False,
    auth_scheme: Optional[AuthScheme] = None,
    auth_credential: Optional[AuthCredential] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> APIHubToolset:
    """
    Create an API Hub toolset.
    
    The APIHubToolset generates tools from a given API Hub resource.
    API Hub is Google Cloud's API management platform that provides
    a central repository for API specifications.
    
    Args:
        apihub_resource_name: Resource name from API Hub.
            Format: projects/{project}/locations/{location}/apis/{api}
            Can optionally include version and spec name.
        access_token: Google access token for API Hub authentication.
        service_account_json: Service account JSON for authentication.
        name: Name of the toolset.
        description: Description of the toolset.
        lazy_load_spec: If True, load spec lazily when needed.
        auth_scheme: Auth scheme for all tools.
        auth_credential: Auth credential for all tools.
        tool_filter: Filter to select specific tools.
    
    Returns:
        APIHubToolset: A configured API Hub toolset.
    
    Example:
        toolset = get_apihub_toolset(
            apihub_resource_name="projects/my-project/locations/us-central1/apis/my-api",
            service_account_json=json.dumps(sa_config)
        )
    """
    settings = get_settings()
    
    return APIHubToolset(
        apihub_resource_name=apihub_resource_name or settings.api_hub.resource_name,
        access_token=access_token,
        service_account_json=service_account_json,
        name=name,
        description=description,
        lazy_load_spec=lazy_load_spec,
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
        tool_filter=tool_filter,
    )


def get_application_integration_toolset(
    project: Optional[str] = None,
    location: Optional[str] = None,
    integration: Optional[str] = None,
    triggers: Optional[List[str]] = None,
    connection: Optional[str] = None,
    entity_operations: Optional[Dict[str, List[str]]] = None,
    actions: Optional[List[str]] = None,
    tool_name_prefix: str = "",
    tool_instructions: str = "",
    service_account_json: Optional[str] = None,
    auth_scheme: Optional[AuthScheme] = None,
    auth_credential: Optional[AuthCredential] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> ApplicationIntegrationToolset:
    """
    Create an Application Integration toolset.
    
    The ApplicationIntegrationToolset generates tools from Application
    Integration or Integration Connector resources. This enables
    agents to interact with enterprise integrations.
    
    Args:
        project: GCP project ID.
        location: GCP location.
        integration: Integration name (for API trigger-based integrations).
        triggers: List of trigger names in the integration.
        connection: Connection name (for connector-based integrations).
        entity_operations: Entity operations supported by the connection.
            Format: {"EntityId": ["LIST", "CREATE", ...]}
        actions: Actions supported by the connection.
        tool_name_prefix: Prefix for tool names.
        tool_instructions: Instructions for the tools.
        service_account_json: Service account JSON for authentication.
        auth_scheme: Auth scheme for all tools.
        auth_credential: Auth credential for all tools.
        tool_filter: Filter to select specific tools.
    
    Returns:
        ApplicationIntegrationToolset: A configured integration toolset.
    
    Example:
        # For integration with API trigger
        toolset = get_application_integration_toolset(
            project="my-project",
            location="us-central1",
            integration="my-integration",
            triggers=["api_trigger/my_trigger"]
        )
        
        # For connector with entity operations
        toolset = get_application_integration_toolset(
            project="my-project",
            location="us-central1",
            connection="my-connection",
            entity_operations={"Users": ["LIST", "CREATE"]},
            actions=["sync_data"]
        )
    """
    settings = get_settings()
    
    return ApplicationIntegrationToolset(
        project=project or settings.app_integration.project,
        location=location or settings.app_integration.location,
        integration=integration or settings.app_integration.integration_name,
        triggers=triggers,
        connection=connection,
        entity_operations=entity_operations,
        actions=actions,
        tool_name_prefix=tool_name_prefix,
        tool_instructions=tool_instructions,
        service_account_json=service_account_json,
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
        tool_filter=tool_filter,
    )


def get_toolbox_toolset(
    server_url: Optional[str] = None,
    toolset_name: Optional[str] = None,
    tool_names: Optional[List[str]] = None,
    auth_token_getters: Optional[Dict[str, Any]] = None,
    bound_params: Optional[Dict[str, Any]] = None,
    credentials: Optional[Any] = None,
    additional_headers: Optional[Dict[str, str]] = None,
) -> ToolboxToolset:
    """
    Create a Toolbox toolset.
    
    The ToolboxToolset provides access to tools from a Toolbox server
    using the MCP Toolbox SDK. Toolbox enables centralized tool
    management and discovery.
    
    Args:
        server_url: URL of the Toolbox server.
        toolset_name: Name of a specific toolset to load.
        tool_names: List of specific tool names to load.
        auth_token_getters: Mapping of auth service names to token getters.
        bound_params: Mapping of parameter names to bound values.
        credentials: Credential configuration.
        additional_headers: Static headers for all requests.
    
    Returns:
        ToolboxToolset: A configured Toolbox toolset.
    
    Example:
        # Load all tools
        toolset = get_toolbox_toolset(
            server_url="http://127.0.0.1:5000"
        )
        
        # Load specific toolset
        toolset = get_toolbox_toolset(
            server_url="http://127.0.0.1:5000",
            toolset_name="my_toolset"
        )
        
        # Load specific tools with auth
        toolset = get_toolbox_toolset(
            server_url="http://127.0.0.1:5000",
            tool_names=["tool1", "tool2"],
            auth_token_getters={"my_service": lambda: "my_token"}
        )
    """
    settings = get_settings()
    
    return ToolboxToolset(
        server_url=server_url or settings.toolbox.server_url,
        toolset_name=toolset_name,
        tool_names=tool_names,
        auth_token_getters=auth_token_getters,
        bound_params=bound_params,
        credentials=credentials,
        additional_headers=additional_headers,
    )


def get_all_enterprise_toolsets() -> List[BaseToolset]:
    """
    Get all configured enterprise toolsets.
    
    Returns a list of enterprise toolsets that are properly configured
    in the environment. Skips toolsets that are not configured.
    
    Returns:
        List[BaseToolset]: List of configured enterprise toolsets.
    """
    settings = get_settings()
    toolsets = []
    
    # API Hub toolset (if configured)
    if settings.api_hub.resource_name:
        try:
            toolsets.append(get_apihub_toolset())
        except Exception:
            pass
    
    # Application Integration (if configured)
    if settings.app_integration.project and settings.app_integration.integration_name:
        try:
            toolsets.append(get_application_integration_toolset())
        except Exception:
            pass
    
    # Toolbox toolset (always available with default URL)
    try:
        toolsets.append(get_toolbox_toolset())
    except Exception:
        pass
    
    return toolsets


# Direct instantiation examples (inline style for variety)

# Example: API Hub toolset with explicit configuration
apihub_example_toolset = APIHubToolset(
    apihub_resource_name="projects/example-project/locations/us-central1/apis/example-api",
    name="Example API Hub Toolset",
    description="Tools generated from Example API in API Hub",
    lazy_load_spec=True,  # Load spec only when tools are accessed
    tool_filter=["get_items", "create_item"],  # Only expose specific operations
)

# Example: Application Integration with entity operations
app_integration_example = ApplicationIntegrationToolset(
    project="example-project",
    location="us-central1",
    connection="salesforce-connection",
    entity_operations={
        "Account": ["LIST", "GET", "CREATE", "UPDATE"],
        "Contact": ["LIST", "GET"],
        "Opportunity": ["LIST", "GET", "CREATE"],
    },
    actions=["sync_accounts"],
    tool_name_prefix="sf_",
    tool_instructions="Use these tools to interact with Salesforce data.",
)

# Example: Application Integration with API trigger
app_integration_trigger_example = ApplicationIntegrationToolset(
    project="example-project",
    location="us-central1",
    integration="order-processing",
    triggers=["api_trigger/process_order", "api_trigger/check_status"],
    tool_name_prefix="order_",
)

# Example: Toolbox with authentication and bound parameters
toolbox_with_auth = ToolboxToolset(
    server_url="http://127.0.0.1:5000",
    toolset_name="secure_tools",
    auth_token_getters={
        "internal_api": lambda: "internal-api-token",
        "external_service": lambda: "external-service-token",
    },
    bound_params={
        "tenant_id": "default-tenant",
        "environment": "production",
    },
    additional_headers={
        "X-Client-Version": "1.0.0",
    },
)
