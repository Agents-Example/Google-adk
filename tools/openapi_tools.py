"""
OpenAPI tools for Google ADK.

This module provides tools for working with OpenAPI specifications:
- OpenAPIToolset: Generate tools from OpenAPI specs
- RestApiTool: Individual REST API tools

OpenAPI integration allows agents to interact with any API that
has an OpenAPI (Swagger) specification.
"""

from typing import Optional, Dict, Any, List, Callable, Union
import ssl

from google.adk.tools.openapi_tool import (
    OpenAPIToolset,
    RestApiTool,
)
from google.adk.auth import AuthConfig, AuthScheme, AuthCredential
from google.adk.tools.base_toolset import ToolPredicate
from google.adk.agents.callback_context import ReadonlyContext

from config.constants import SAMPLE_OPENAPI_SPEC


def create_openapi_toolset(
    spec_dict: Optional[Dict] = None,
    spec_str: Optional[str] = None,
    spec_str_type: str = "json",
    auth_scheme: Optional[AuthScheme] = None,
    auth_credential: Optional[AuthCredential] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
    tool_name_prefix: Optional[str] = None,
    ssl_verify: Optional[Union[bool, str, ssl.SSLContext]] = None,
    header_provider: Optional[Callable[[ReadonlyContext], Dict[str, str]]] = None,
) -> OpenAPIToolset:
    """
    Create an OpenAPI toolset from a specification.
    
    The OpenAPIToolset parses an OpenAPI spec and generates tools
    for each operation defined in the spec.
    
    Args:
        spec_dict: OpenAPI spec as a dictionary.
        spec_str: OpenAPI spec as a JSON or YAML string.
        spec_str_type: Type of spec_str ("json" or "yaml").
        auth_scheme: Authentication scheme for all tools.
        auth_credential: Authentication credential for all tools.
        tool_filter: Filter to select specific tools.
        tool_name_prefix: Prefix for tool names.
        ssl_verify: SSL verification option.
        header_provider: Function to provide dynamic headers.
    
    Returns:
        OpenAPIToolset: A configured OpenAPI toolset.
    
    Example:
        # From dictionary
        toolset = create_openapi_toolset(spec_dict=my_spec)
        
        # From JSON string
        toolset = create_openapi_toolset(
            spec_str=json_spec,
            spec_str_type="json"
        )
        
        # With authentication
        toolset = create_openapi_toolset(
            spec_dict=my_spec,
            auth_scheme=my_auth_scheme,
            auth_credential=my_credential
        )
    """
    return OpenAPIToolset(
        spec_dict=spec_dict,
        spec_str=spec_str,
        spec_str_type=spec_str_type,
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
        ssl_verify=ssl_verify,
        header_provider=header_provider,
    )


def create_rest_api_tool(
    name: str,
    description: str,
    base_url: str,
    path: str,
    method: str = "GET",
    parameters: Optional[List[Dict]] = None,
    request_body: Optional[Dict] = None,
    auth_scheme: Optional[AuthScheme] = None,
    auth_credential: Optional[AuthCredential] = None,
    ssl_verify: Optional[Union[bool, str, ssl.SSLContext]] = None,
    header_provider: Optional[Callable[[ReadonlyContext], Dict[str, str]]] = None,
) -> RestApiTool:
    """
    Create a single REST API tool manually.
    
    This is useful when you want to create a tool for a specific
    API endpoint without a full OpenAPI spec.
    
    Args:
        name: Name of the tool.
        description: Description of what the tool does.
        base_url: Base URL of the API.
        path: Path of the endpoint (e.g., "/users/{id}").
        method: HTTP method (GET, POST, PUT, DELETE, etc.).
        parameters: List of parameter definitions.
        request_body: Request body schema.
        auth_scheme: Authentication scheme.
        auth_credential: Authentication credential.
        ssl_verify: SSL verification option.
        header_provider: Function to provide dynamic headers.
    
    Returns:
        RestApiTool: A configured REST API tool.
    
    Example:
        tool = create_rest_api_tool(
            name="get_user",
            description="Get a user by ID",
            base_url="https://api.example.com",
            path="/users/{user_id}",
            method="GET",
            parameters=[{
                "name": "user_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string"}
            }]
        )
    """
    # Build operation spec
    operation = {
        "operationId": name,
        "summary": description,
        "parameters": parameters or [],
    }
    
    if request_body:
        operation["requestBody"] = request_body
    
    # Build endpoint
    endpoint = {
        "base_url": base_url,
        "path": path,
        "method": method.upper(),
    }
    
    tool = RestApiTool(
        name=name,
        description=description,
        endpoint=endpoint,
        operation=operation,
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
        ssl_verify=ssl_verify,
        header_provider=header_provider,
    )
    
    return tool


def get_sample_openapi_toolset() -> OpenAPIToolset:
    """
    Get a sample OpenAPI toolset for demonstration.
    
    Uses the sample OpenAPI spec from constants to create
    a toolset with example API operations.
    
    Returns:
        OpenAPIToolset: A sample toolset for demonstration.
    
    Example:
        sample = get_sample_openapi_toolset()
        tools = await sample.get_tools()
    """
    return OpenAPIToolset(
        spec_dict=SAMPLE_OPENAPI_SPEC,
        tool_name_prefix="sample_api_",
    )


# Example: Creating toolset from YAML string
PETSTORE_YAML_SPEC = """
openapi: "3.0.0"
info:
  title: Petstore API
  version: "1.0.0"
servers:
  - url: https://petstore.example.com/v1
paths:
  /pets:
    get:
      operationId: list_pets
      summary: List all pets
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            maximum: 100
      responses:
        "200":
          description: A list of pets
    post:
      operationId: create_pet
      summary: Create a pet
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                tag:
                  type: string
      responses:
        "201":
          description: Pet created
  /pets/{petId}:
    get:
      operationId: get_pet
      summary: Get a pet by ID
      parameters:
        - name: petId
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: A pet
"""

# Direct instantiation example (inline style)
petstore_toolset = OpenAPIToolset(
    spec_str=PETSTORE_YAML_SPEC,
    spec_str_type="yaml",
    tool_name_prefix="petstore_",
)


# Example: Creating multiple REST API tools manually
def get_manual_rest_api_tools() -> List[RestApiTool]:
    """
    Get manually defined REST API tools.
    
    Demonstrates creating REST API tools without OpenAPI spec.
    """
    return [
        # Weather API
        RestApiTool(
            name="get_weather",
            description="Get current weather for a city",
            endpoint={
                "base_url": "https://api.weather.example.com",
                "path": "/current",
                "method": "GET",
            },
            operation={
                "operationId": "get_weather",
                "summary": "Get current weather",
                "parameters": [
                    {
                        "name": "city",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "units",
                        "in": "query",
                        "schema": {"type": "string", "enum": ["metric", "imperial"]}
                    }
                ]
            },
        ),
        
        # User API
        RestApiTool(
            name="get_user_profile",
            description="Get a user's profile by username",
            endpoint={
                "base_url": "https://api.example.com",
                "path": "/users/{username}",
                "method": "GET",
            },
            operation={
                "operationId": "get_user_profile",
                "summary": "Get user profile",
                "parameters": [
                    {
                        "name": "username",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            },
        ),
    ]


# Example: Dynamic header provider for API authentication
def api_key_header_provider(ctx: ReadonlyContext) -> Dict[str, str]:
    """
    Provides API key header from session state.
    """
    api_key = ctx.state.get("api_key", "")
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }


# Example: Custom SSL context for enterprise proxies
def create_enterprise_ssl_context() -> ssl.SSLContext:
    """
    Create SSL context for enterprise environments with custom CA.
    """
    context = ssl.create_default_context()
    # In production, load your enterprise CA certificate
    # context.load_verify_locations('/path/to/enterprise-ca.crt')
    return context
