"""
MCP (Model Context Protocol) integrations for Google ADK.

Provides setup functions and configurations for all MCP server integrations:
- GitHub: Code management, issues, PRs
- Hugging Face: Models, datasets, research papers
- Notion: Workspace management, pages, databases
- Stripe: Payments, customers, subscriptions
- ElevenLabs: Speech generation, voice cloning
- PayPal: Payment processing
- Linear: Issue tracking
- Atlassian: Jira, Confluence
- Asana: Task management
- GitLab: Code management
- Postman: API testing
- N8N: Workflow automation
- Daytona: Development environments
- Cartesia: Speech generation, voice localization
- Chroma: Vector store, semantic search
- Qdrant: Vector search engine
- MongoDB: Document database, Atlas management
"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from mcp import StdioServerParameters


# =============================================================================
# GitHub MCP Integration
# =============================================================================

@dataclass
class GitHubMCPConfig:
    """Configuration for GitHub MCP integration."""
    token: Optional[str] = None
    toolsets: str = "all"
    readonly: bool = True
    use_remote: bool = True
    remote_url: str = "https://api.githubcopilot.com/mcp/"
    
    def __post_init__(self):
        self.token = self.token or os.getenv("GITHUB_TOKEN")


github_mcp_config = GitHubMCPConfig()


def get_github_mcp_toolset(
    token: Optional[str] = None,
    toolsets: str = "all",
    readonly: bool = True,
    use_remote: bool = True,
) -> McpToolset:
    """
    Get GitHub MCP toolset.
    
    GitHub MCP provides tools for repository management, issues, PRs, and code analysis.
    
    Args:
        token: GitHub personal access token.
        toolsets: Comma-separated list of toolsets (repos, issues, pull_requests, etc.)
        readonly: Enable only read operations.
        use_remote: Use remote MCP server (recommended).
    
    Returns:
        McpToolset: Configured GitHub MCP toolset.
    
    Available toolsets:
        - repos, issues, pull_requests, actions, discussions
        - code_security, dependabot, gists, labels, notifications
        - orgs, projects, users, stargazers
    """
    token = token or os.getenv("GITHUB_TOKEN")
    
    if use_remote:
        return McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-MCP-Toolsets": toolsets,
                    "X-MCP-Readonly": str(readonly).lower(),
                },
            ),
        )
    else:
        return McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@github/mcp-server"],
                    env={"GITHUB_TOKEN": token},
                ),
            ),
        )


# =============================================================================
# Hugging Face MCP Integration
# =============================================================================

@dataclass
class HuggingFaceMCPConfig:
    """Configuration for Hugging Face MCP integration."""
    token: Optional[str] = None
    use_remote: bool = True
    remote_url: str = "https://huggingface.co/mcp"
    
    def __post_init__(self):
        self.token = self.token or os.getenv("HF_TOKEN")


huggingface_mcp_config = HuggingFaceMCPConfig()


def get_huggingface_mcp_toolset(
    token: Optional[str] = None,
    use_remote: bool = True,
) -> McpToolset:
    """
    Get Hugging Face MCP toolset.
    
    Hugging Face MCP provides access to models, datasets, and AI applications.
    
    Args:
        token: Hugging Face access token.
        use_remote: Use remote MCP server.
    
    Returns:
        McpToolset: Configured Hugging Face MCP toolset.
    
    Available tools:
        - Spaces Semantic Search, Papers Semantic Search
        - Model Search, Dataset Search, Documentation Search
        - Hub Repository Details
    """
    token = token or os.getenv("HF_TOKEN")
    
    if use_remote:
        return McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://huggingface.co/mcp",
                headers={"Authorization": f"Bearer {token}"},
            ),
        )
    else:
        return McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@llmindset/hf-mcp-server"],
                    env={"HF_TOKEN": token},
                ),
                timeout=30,
            ),
        )


# =============================================================================
# Notion MCP Integration
# =============================================================================

@dataclass
class NotionMCPConfig:
    """Configuration for Notion MCP integration."""
    token: Optional[str] = None
    
    def __post_init__(self):
        self.token = self.token or os.getenv("NOTION_TOKEN")


notion_mcp_config = NotionMCPConfig()


def get_notion_mcp_toolset(token: Optional[str] = None) -> McpToolset:
    """
    Get Notion MCP toolset.
    
    Notion MCP provides workspace search, page creation, and database management.
    
    Args:
        token: Notion integration token.
    
    Returns:
        McpToolset: Configured Notion MCP toolset.
    
    Available tools:
        - notion-search, notion-fetch, notion-create-pages
        - notion-update-page, notion-move-pages, notion-duplicate-page
        - notion-create-database, notion-update-database
        - notion-create-comment, notion-get-comments
        - notion-get-teams, notion-get-users
    """
    token = token or os.getenv("NOTION_TOKEN")
    
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@notionhq/notion-mcp-server"],
                env={"NOTION_TOKEN": token},
            ),
            timeout=30,
        ),
    )


# =============================================================================
# Stripe MCP Integration
# =============================================================================

@dataclass
class StripeMCPConfig:
    """Configuration for Stripe MCP integration."""
    secret_key: Optional[str] = None
    tools: str = "all"
    use_remote: bool = True
    remote_url: str = "https://mcp.stripe.com"
    
    def __post_init__(self):
        self.secret_key = self.secret_key or os.getenv("STRIPE_SECRET_KEY")


stripe_mcp_config = StripeMCPConfig()


def get_stripe_mcp_toolset(
    secret_key: Optional[str] = None,
    tools: str = "all",
    use_remote: bool = True,
) -> McpToolset:
    """
    Get Stripe MCP toolset.
    
    Stripe MCP provides payment management, customer operations, and invoicing.
    
    Args:
        secret_key: Stripe secret API key.
        tools: Comma-separated list of tools to enable.
        use_remote: Use remote MCP server.
    
    Returns:
        McpToolset: Configured Stripe MCP toolset.
    
    Available tools:
        - Account: get_stripe_account_info
        - Balance: retrieve_balance
        - Customer: create_customer, list_customers
        - Invoice: create_invoice, finalize_invoice, list_invoices
        - Payment: create_payment_link, list_payment_intents
        - Product: create_product, list_products, create_price
        - Subscription: list_subscriptions, update_subscription
    """
    secret_key = secret_key or os.getenv("STRIPE_SECRET_KEY")
    
    if use_remote:
        return McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://mcp.stripe.com",
                headers={"Authorization": f"Bearer {secret_key}"},
            ),
        )
    else:
        return McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@stripe/mcp", f"--tools={tools}"],
                    env={"STRIPE_SECRET_KEY": secret_key},
                ),
                timeout=30,
            ),
        )


# =============================================================================
# ElevenLabs MCP Integration
# =============================================================================

@dataclass
class ElevenLabsMCPConfig:
    """Configuration for ElevenLabs MCP integration."""
    api_key: Optional[str] = None
    output_mode: str = "files"  # files, resources, or both
    base_path: str = "~/Desktop"
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("ELEVENLABS_API_KEY")


elevenlabs_mcp_config = ElevenLabsMCPConfig()


def get_elevenlabs_mcp_toolset(api_key: Optional[str] = None) -> McpToolset:
    """
    Get ElevenLabs MCP toolset.
    
    ElevenLabs MCP provides text-to-speech, voice cloning, and audio processing.
    
    Args:
        api_key: ElevenLabs API key.
    
    Returns:
        McpToolset: Configured ElevenLabs MCP toolset.
    
    Available tools:
        - Text-to-speech: text_to_speech, speech_to_speech
        - Voice: voice_clone, get_voice, search_voices
        - Audio: speech_to_text, text_to_sound_effects, isolate_audio
        - Conversational AI: create_agent, make_outbound_call
    """
    api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
    
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uvx",
                args=["elevenlabs-mcp"],
                env={"ELEVENLABS_API_KEY": api_key},
            ),
            timeout=30,
        ),
    )


# =============================================================================
# PayPal MCP Integration
# =============================================================================

@dataclass
class PayPalMCPConfig:
    """Configuration for PayPal MCP integration."""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    
    def __post_init__(self):
        self.client_id = self.client_id or os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = self.client_secret or os.getenv("PAYPAL_CLIENT_SECRET")


paypal_mcp_config = PayPalMCPConfig()


def get_paypal_mcp_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> McpToolset:
    """Get PayPal MCP toolset for payment processing."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-paypal"],
                env={
                    "PAYPAL_CLIENT_ID": client_id or os.getenv("PAYPAL_CLIENT_ID"),
                    "PAYPAL_CLIENT_SECRET": client_secret or os.getenv("PAYPAL_CLIENT_SECRET"),
                },
            ),
        ),
    )


# =============================================================================
# Linear MCP Integration
# =============================================================================

@dataclass
class LinearMCPConfig:
    """Configuration for Linear MCP integration."""
    api_key: Optional[str] = None
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("LINEAR_API_KEY")


linear_mcp_config = LinearMCPConfig()


def get_linear_mcp_toolset(api_key: Optional[str] = None) -> McpToolset:
    """Get Linear MCP toolset for issue tracking."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-linear"],
                env={"LINEAR_API_KEY": api_key or os.getenv("LINEAR_API_KEY")},
            ),
        ),
    )


# =============================================================================
# Atlassian MCP Integration
# =============================================================================

@dataclass
class AtlassianMCPConfig:
    """Configuration for Atlassian MCP integration."""
    email: Optional[str] = None
    api_token: Optional[str] = None
    base_url: Optional[str] = None
    
    def __post_init__(self):
        self.email = self.email or os.getenv("ATLASSIAN_EMAIL")
        self.api_token = self.api_token or os.getenv("ATLASSIAN_API_TOKEN")
        self.base_url = self.base_url or os.getenv("ATLASSIAN_BASE_URL")


atlassian_mcp_config = AtlassianMCPConfig()


def get_atlassian_mcp_toolset(
    email: Optional[str] = None,
    api_token: Optional[str] = None,
    base_url: Optional[str] = None,
) -> McpToolset:
    """Get Atlassian MCP toolset for Jira and Confluence."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-atlassian"],
                env={
                    "ATLASSIAN_EMAIL": email or os.getenv("ATLASSIAN_EMAIL"),
                    "ATLASSIAN_API_TOKEN": api_token or os.getenv("ATLASSIAN_API_TOKEN"),
                    "ATLASSIAN_BASE_URL": base_url or os.getenv("ATLASSIAN_BASE_URL"),
                },
            ),
        ),
    )


# =============================================================================
# Asana MCP Integration
# =============================================================================

@dataclass
class AsanaMCPConfig:
    """Configuration for Asana MCP integration."""
    access_token: Optional[str] = None
    
    def __post_init__(self):
        self.access_token = self.access_token or os.getenv("ASANA_ACCESS_TOKEN")


asana_mcp_config = AsanaMCPConfig()


def get_asana_mcp_toolset(access_token: Optional[str] = None) -> McpToolset:
    """Get Asana MCP toolset for task management."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-asana"],
                env={"ASANA_ACCESS_TOKEN": access_token or os.getenv("ASANA_ACCESS_TOKEN")},
            ),
        ),
    )


# =============================================================================
# GitLab MCP Integration
# =============================================================================

@dataclass
class GitLabMCPConfig:
    """Configuration for GitLab MCP integration."""
    token: Optional[str] = None
    base_url: str = "https://gitlab.com"
    
    def __post_init__(self):
        self.token = self.token or os.getenv("GITLAB_TOKEN")


gitlab_mcp_config = GitLabMCPConfig()


def get_gitlab_mcp_toolset(
    token: Optional[str] = None,
    base_url: str = "https://gitlab.com",
) -> McpToolset:
    """Get GitLab MCP toolset for code management."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-gitlab"],
                env={
                    "GITLAB_TOKEN": token or os.getenv("GITLAB_TOKEN"),
                    "GITLAB_BASE_URL": base_url,
                },
            ),
        ),
    )


# =============================================================================
# Postman MCP Integration
# =============================================================================

@dataclass
class PostmanMCPConfig:
    """Configuration for Postman MCP integration."""
    api_key: Optional[str] = None
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("POSTMAN_API_KEY")


postman_mcp_config = PostmanMCPConfig()


def get_postman_mcp_toolset(api_key: Optional[str] = None) -> McpToolset:
    """Get Postman MCP toolset for API testing."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-postman"],
                env={"POSTMAN_API_KEY": api_key or os.getenv("POSTMAN_API_KEY")},
            ),
        ),
    )


# =============================================================================
# N8N MCP Integration
# =============================================================================

@dataclass
class N8NMCPConfig:
    """Configuration for N8N MCP integration."""
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("N8N_API_KEY")
        self.base_url = self.base_url or os.getenv("N8N_BASE_URL")


n8n_mcp_config = N8NMCPConfig()


def get_n8n_mcp_toolset(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> McpToolset:
    """Get N8N MCP toolset for workflow automation."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-n8n"],
                env={
                    "N8N_API_KEY": api_key or os.getenv("N8N_API_KEY"),
                    "N8N_BASE_URL": base_url or os.getenv("N8N_BASE_URL"),
                },
            ),
        ),
    )


# =============================================================================
# Daytona MCP Integration
# =============================================================================

@dataclass
class DaytonaMCPConfig:
    """Configuration for Daytona MCP integration."""
    api_key: Optional[str] = None
    
    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("DAYTONA_API_KEY")


daytona_mcp_config = DaytonaMCPConfig()


def get_daytona_mcp_toolset(api_key: Optional[str] = None) -> McpToolset:
    """Get Daytona MCP toolset for development environments."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@anthropic/mcp-server-daytona"],
                env={"DAYTONA_API_KEY": api_key or os.getenv("DAYTONA_API_KEY")},
            ),
        ),
    )


# =============================================================================
# Cartesia MCP Integration
# =============================================================================

@dataclass
class CartesiaMCPConfig:
    """Configuration for Cartesia MCP integration."""
    api_key: Optional[str] = None
    output_directory: Optional[str] = None

    def __post_init__(self):
        self.api_key = self.api_key or os.getenv("CARTESIA_API_KEY")


cartesia_mcp_config = CartesiaMCPConfig()


def get_cartesia_mcp_toolset(
    api_key: Optional[str] = None,
    output_directory: Optional[str] = None,
) -> McpToolset:
    """
    Get Cartesia MCP toolset for speech generation and voice localization.

    Cartesia provides text-to-speech, voice cloning, voice change, and audio infill.
    """
    env = {"CARTESIA_API_KEY": api_key or os.getenv("CARTESIA_API_KEY")}
    if output_directory:
        env["OUTPUT_DIRECTORY"] = output_directory
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uvx",
                args=["cartesia-mcp"],
                env=env,
            ),
            timeout=30,
        ),
    )


# =============================================================================
# Chroma MCP Integration
# =============================================================================

@dataclass
class ChromaMCPConfig:
    """Configuration for Chroma MCP integration."""
    data_dir: Optional[str] = None
    client_type: str = "persistent"
    tenant: Optional[str] = None
    database: Optional[str] = None
    api_key: Optional[str] = None

    def __post_init__(self):
        self.data_dir = self.data_dir or os.getenv("CHROMA_DATA_DIR")
        self.tenant = self.tenant or os.getenv("CHROMA_TENANT")
        self.database = self.database or os.getenv("CHROMA_DATABASE")
        self.api_key = self.api_key or os.getenv("CHROMA_API_KEY")


chroma_mcp_config = ChromaMCPConfig()


def get_chroma_mcp_toolset(
    data_dir: Optional[str] = None,
    client_type: str = "persistent",
    tenant: Optional[str] = None,
    database: Optional[str] = None,
    api_key: Optional[str] = None,
) -> McpToolset:
    """
    Get Chroma MCP toolset for vector store and semantic search.

    Use data_dir for local persistent storage, or tenant/database/api_key for Chroma Cloud.
    """
    args = ["chroma-mcp", "--client-type", client_type or "persistent"]
    env = {}
    if data_dir or os.getenv("CHROMA_DATA_DIR"):
        args.extend(["--data-dir", data_dir or os.getenv("CHROMA_DATA_DIR")])
    if client_type == "cloud" and (tenant or database or api_key):
        if tenant:
            args.extend(["--tenant", tenant])
        if database:
            args.extend(["--database", database])
        if api_key:
            env["CHROMA_API_KEY"] = api_key
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uvx",
                args=args,
                env=env or None,
            ),
            timeout=30,
        ),
    )


# =============================================================================
# Qdrant MCP Integration
# =============================================================================

@dataclass
class QdrantMCPConfig:
    """Configuration for Qdrant MCP integration."""
    url: Optional[str] = None
    collection_name: Optional[str] = None
    api_key: Optional[str] = None

    def __post_init__(self):
        self.url = self.url or os.getenv("QDRANT_URL")
        self.collection_name = self.collection_name or os.getenv("COLLECTION_NAME")
        self.api_key = self.api_key or os.getenv("QDRANT_API_KEY")


qdrant_mcp_config = QdrantMCPConfig()


def get_qdrant_mcp_toolset(
    url: Optional[str] = None,
    collection_name: Optional[str] = None,
    api_key: Optional[str] = None,
) -> McpToolset:
    """
    Get Qdrant MCP toolset for vector search and semantic memory.
    """
    env = {
        "QDRANT_URL": url or os.getenv("QDRANT_URL", "http://localhost:6333"),
        "COLLECTION_NAME": collection_name or os.getenv("COLLECTION_NAME", "default"),
    }
    if api_key or os.getenv("QDRANT_API_KEY"):
        env["QDRANT_API_KEY"] = api_key or os.getenv("QDRANT_API_KEY")
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uvx",
                args=["mcp-server-qdrant"],
                env=env,
            ),
            timeout=30,
        ),
    )


# =============================================================================
# MongoDB MCP Integration
# =============================================================================

@dataclass
class MongoDBMCPConfig:
    """Configuration for MongoDB MCP integration."""
    connection_string: Optional[str] = None
    read_only: bool = False
    atlas_client_id: Optional[str] = None
    atlas_client_secret: Optional[str] = None

    def __post_init__(self):
        self.connection_string = self.connection_string or os.getenv("MDB_MCP_CONNECTION_STRING")
        self.atlas_client_id = self.atlas_client_id or os.getenv("MDB_MCP_API_CLIENT_ID")
        self.atlas_client_secret = self.atlas_client_secret or os.getenv("MDB_MCP_API_CLIENT_SECRET")


mongodb_mcp_config = MongoDBMCPConfig()


def get_mongodb_mcp_toolset(
    connection_string: Optional[str] = None,
    read_only: bool = True,
    atlas_client_id: Optional[str] = None,
    atlas_client_secret: Optional[str] = None,
) -> McpToolset:
    """
    Get MongoDB MCP toolset for querying collections, managing databases, and Atlas.
    """
    args = ["-y", "mongodb-mcp-server"]
    if read_only:
        args.append("--readOnly")
    env = {
        "MDB_MCP_CONNECTION_STRING": connection_string or os.getenv("MDB_MCP_CONNECTION_STRING", "mongodb://localhost:27017"),
    }
    if atlas_client_id or os.getenv("MDB_MCP_API_CLIENT_ID"):
        env["MDB_MCP_API_CLIENT_ID"] = atlas_client_id or os.getenv("MDB_MCP_API_CLIENT_ID")
    if atlas_client_secret or os.getenv("MDB_MCP_API_CLIENT_SECRET"):
        env["MDB_MCP_API_CLIENT_SECRET"] = atlas_client_secret or os.getenv("MDB_MCP_API_CLIENT_SECRET")
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=args,
                env=env,
            ),
            timeout=30,
        ),
    )
