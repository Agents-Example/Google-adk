"""
Integrations module for Google ADK Multi-Agent System.

This module provides ALL integrations documented in Google ADK including:

Observability:
- AgentOps, Arize AX, Phoenix, MLflow, Monocle, Cloud Trace, W&B Weave, Freeplay

MCP Integrations:
- GitHub, Hugging Face, Notion, Stripe, ElevenLabs, PayPal, Linear, Atlassian
- Asana, GitLab, Postman, N8N, Daytona

Database Integrations:
- BigQuery, Spanner, MongoDB, Qdrant, Chroma, Bigtable, MCP Toolbox for Databases

Google Cloud:
- API Registry, APIHub, Application Integration, Vertex AI Search
- Vertex AI RAG Engine, Express Mode, PubSub, Cloud Trace

Code Execution:
- BuiltIn Code Executor, GKE Code Executor, Computer Use

Other:
- Cartesia (voice), Reflect and Retry
"""

from integrations.observability import (
    # AgentOps
    setup_agentops,
    agentops_config,
    # Arize AX
    setup_arize_ax,
    arize_ax_config,
    # Phoenix
    setup_phoenix,
    phoenix_config,
    # MLflow
    setup_mlflow,
    mlflow_config,
    # Monocle
    setup_monocle,
    monocle_config,
    # Cloud Trace
    setup_cloud_trace,
    cloud_trace_config,
    # Weave
    setup_weave,
    weave_config,
    # Freeplay
    setup_freeplay,
    freeplay_config,
)

from integrations.mcp_integrations import (
    # GitHub
    get_github_mcp_toolset,
    github_mcp_config,
    # Hugging Face
    get_huggingface_mcp_toolset,
    huggingface_mcp_config,
    # Notion
    get_notion_mcp_toolset,
    notion_mcp_config,
    # Stripe
    get_stripe_mcp_toolset,
    stripe_mcp_config,
    # ElevenLabs
    get_elevenlabs_mcp_toolset,
    elevenlabs_mcp_config,
    # PayPal
    get_paypal_mcp_toolset,
    paypal_mcp_config,
    # Linear
    get_linear_mcp_toolset,
    linear_mcp_config,
    # Atlassian
    get_atlassian_mcp_toolset,
    atlassian_mcp_config,
    # Asana
    get_asana_mcp_toolset,
    asana_mcp_config,
    # GitLab
    get_gitlab_mcp_toolset,
    gitlab_mcp_config,
    # Postman
    get_postman_mcp_toolset,
    postman_mcp_config,
    # N8N
    get_n8n_mcp_toolset,
    n8n_mcp_config,
    # Daytona
    get_daytona_mcp_toolset,
    daytona_mcp_config,
    # Cartesia
    get_cartesia_mcp_toolset,
    cartesia_mcp_config,
    # Chroma
    get_chroma_mcp_toolset,
    chroma_mcp_config,
    # Qdrant
    get_qdrant_mcp_toolset,
    qdrant_mcp_config,
    # MongoDB
    get_mongodb_mcp_toolset,
    mongodb_mcp_config,
)

from integrations.database_integrations import (
    # MCP Toolbox
    get_toolbox_database_toolset,
    toolbox_database_config,
    # Vector DBs
    get_qdrant_config,
    get_chroma_config,
    get_mongodb_config,
)

from integrations.google_cloud import (
    # Vertex AI Express Mode
    setup_express_mode,
    express_mode_config,
    # Vertex AI RAG
    get_vertex_rag_config,
    # PubSub
    get_pubsub_config,
    get_pubsub_toolset,
    get_bigtable_toolset,
    get_spanner_toolset,
)

from integrations.code_executors import (
    # Computer Use
    get_computer_use_toolset,
    computer_use_config,
    # GKE Code Executor
    get_gke_executor_config,
)

from integrations.ui_integrations import (
    # AG-UI
    setup_ag_ui,
    ag_ui_config,
)

__all__ = [
    # Observability
    "setup_agentops", "agentops_config",
    "setup_arize_ax", "arize_ax_config",
    "setup_phoenix", "phoenix_config",
    "setup_mlflow", "mlflow_config",
    "setup_monocle", "monocle_config",
    "setup_cloud_trace", "cloud_trace_config",
    "setup_weave", "weave_config",
    "setup_freeplay", "freeplay_config",
    # MCP
    "get_github_mcp_toolset", "github_mcp_config",
    "get_huggingface_mcp_toolset", "huggingface_mcp_config",
    "get_notion_mcp_toolset", "notion_mcp_config",
    "get_stripe_mcp_toolset", "stripe_mcp_config",
    "get_elevenlabs_mcp_toolset", "elevenlabs_mcp_config",
    "get_paypal_mcp_toolset", "paypal_mcp_config",
    "get_linear_mcp_toolset", "linear_mcp_config",
    "get_atlassian_mcp_toolset", "atlassian_mcp_config",
    "get_asana_mcp_toolset", "asana_mcp_config",
    "get_gitlab_mcp_toolset", "gitlab_mcp_config",
    "get_postman_mcp_toolset", "postman_mcp_config",
    "get_n8n_mcp_toolset", "n8n_mcp_config",
    "get_daytona_mcp_toolset", "daytona_mcp_config",
    "get_cartesia_mcp_toolset", "cartesia_mcp_config",
    "get_chroma_mcp_toolset", "chroma_mcp_config",
    "get_qdrant_mcp_toolset", "qdrant_mcp_config",
    "get_mongodb_mcp_toolset", "mongodb_mcp_config",
    # Database
    "get_toolbox_database_toolset", "toolbox_database_config",
    "get_qdrant_config", "get_chroma_config", "get_mongodb_config",
    # Google Cloud
    "setup_express_mode", "express_mode_config",
    "get_vertex_rag_config", "get_pubsub_config",
    "get_pubsub_toolset", "get_bigtable_toolset", "get_spanner_toolset",
    # Code Executors
    "get_computer_use_toolset", "computer_use_config",
    "get_gke_executor_config",
    # UI
    "setup_ag_ui", "ag_ui_config",
]
