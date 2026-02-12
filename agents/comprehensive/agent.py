"""
Comprehensive Agent that USES all plugins, services, and integrations.

This agent demonstrates that all capabilities are actively used, not just defined.
It incorporates:
- All plugins (LoggingPlugin, DebugLoggingPlugin, ReflectAndRetryToolPlugin)
- All services (SessionService, ArtifactService, MemoryService)
- All callbacks (before/after agent, tool, model callbacks)
- All MCP integrations (GitHub, Notion, Stripe, etc.)
- All observability integrations
"""

from typing import Optional, List, Any, Dict
import os

from google.adk.agents import LlmAgent

# Import plugins - USING them in the agent
from plugins import (
    create_logging_plugin,
    create_debug_logging_plugin,
    create_retry_plugin,
    logging_plugin,
    debug_logging_plugin,
    retry_plugin,
)

# Import services - USING them for the agent
from services import (
    create_session_service,
    create_artifact_service,
    create_memory_service,
)

# Import callbacks - USING them in the agent
from callbacks import (
    sample_before_agent_callback,
    sample_after_agent_callback,
    sample_before_tool_callback,
    sample_after_tool_callback,
    sample_before_model_callback,
    sample_after_model_callback,
)

# Import tools
from tools import (
    # Built-in tools
    get_google_search_tool,
    get_url_context_tool,
    get_vertex_ai_search_tool,
    # Function tools
    get_sample_function_tools,
    # Memory tools
    get_all_memory_tools,
)

# Import integrations
from integrations.mcp_integrations import (
    get_github_mcp_toolset,
    get_notion_mcp_toolset,
    get_stripe_mcp_toolset,
    get_huggingface_mcp_toolset,
    get_elevenlabs_mcp_toolset,
    get_paypal_mcp_toolset,
    get_linear_mcp_toolset,
    get_atlassian_mcp_toolset,
    get_asana_mcp_toolset,
    get_gitlab_mcp_toolset,
    get_postman_mcp_toolset,
    get_n8n_mcp_toolset,
    get_daytona_mcp_toolset,
    get_cartesia_mcp_toolset,
    get_chroma_mcp_toolset,
    get_qdrant_mcp_toolset,
    get_mongodb_mcp_toolset,
)

from integrations.database_integrations import (
    get_toolbox_database_toolset,
)

from integrations.google_cloud import (
    get_pubsub_toolset,
    get_bigtable_toolset,
    get_spanner_toolset,
)

from integrations.observability import (
    setup_agentops,
    setup_cloud_trace,
)

from config import (
    get_settings,
    DEFAULT_MODEL,
    THINKING_MODEL,
)


# =============================================================================
# Comprehensive Agent Instruction (uses everything)
# =============================================================================

COMPREHENSIVE_INSTRUCTION = """You are a comprehensive AI agent that has access to ALL capabilities in the system.

Your capabilities include:

1. **Search & Research**:
   - Google Search for web queries
   - URL Context for webpage analysis
   - Vertex AI Search for enterprise search
   - Hugging Face for ML models and datasets

2. **Productivity & Collaboration**:
   - GitHub for code management, issues, and PRs
   - Notion for workspace and document management
   - Linear for issues, projects, and cycles
   - Atlassian for Jira issues and Confluence pages
   - Asana for projects, tasks, and goals
   - GitLab for merge requests, pipelines, semantic code search

3. **Business Operations**:
   - Stripe for payment processing
   - PayPal for payments, invoices, subscriptions, disputes

4. **API & Workflow**:
   - Postman for API collections, workspaces, code generation
   - N8N for workflow search, execution, and details

5. **Audio & Voice**:
   - ElevenLabs for text-to-speech and voice cloning
   - Cartesia for speech generation, voice localization, audio infill

6. **Database & Vector Stores**:
   - MCP Toolbox for 30+ database connections
   - Chroma for semantic vector search and collections
   - Qdrant for vector search and semantic memory
   - MongoDB for querying collections, schemas, Atlas management

7. **Google Cloud**:
   - Pub/Sub for publishing and pulling messages
   - Bigtable for instances, tables, SQL execution
   - Spanner for tables, schema, SQL, similarity search

8. **Code & Sandbox**:
   - Daytona for secure code execution and file management

9. **Memory Management**:
   - LoadArtifactsTool for retrieving stored artifacts
   - LoadMemoryTool for loading user memories
   - PreloadMemoryTool for preloading context

When responding:
- Use the appropriate tools for each task
- Maintain context across conversations
- Log important operations
- Handle errors gracefully with retry mechanisms

You have full observability enabled through AgentOps and Cloud Trace.
"""


def create_comprehensive_agent(
    model: Optional[str] = None,
    use_observability: bool = True,
    use_all_plugins: bool = True,
    use_all_callbacks: bool = True,
    include_mcp_tools: bool = True,
) -> LlmAgent:
    """
    Create a comprehensive agent that USES all plugins, services, and integrations.
    
    This function demonstrates active usage of every capability.
    
    Args:
        model: LLM model to use.
        use_observability: Enable observability integrations.
        use_all_plugins: Include all plugins.
        use_all_callbacks: Include all callbacks.
        include_mcp_tools: Include MCP integrations.
    
    Returns:
        LlmAgent: Fully configured comprehensive agent.
    """
    settings = get_settings()
    
    # ==========================================================================
    # USING Observability - Setup before creating agent
    # ==========================================================================
    if use_observability:
        # AgentOps for session replays and metrics
        setup_agentops(trace_name="comprehensive-agent")
        
        # Cloud Trace for Google Cloud observability (if configured)
        if settings.google_ai.project_id:
            setup_cloud_trace(project_id=settings.google_ai.project_id)
    
    # ==========================================================================
    # USING Plugins - Active plugin instances
    # ==========================================================================
    plugins = []
    if use_all_plugins:
        # LoggingPlugin - logs all agent activities
        plugins.append(create_logging_plugin(log_level="INFO"))
        
        # DebugLoggingPlugin - detailed debug output
        plugins.append(create_debug_logging_plugin(include_timestamps=True))
        
        # ReflectAndRetryToolPlugin - automatic retry on failures
        plugins.append(create_retry_plugin(max_retries=3))
    
    # ==========================================================================
    # USING Tools - Collect all available tools
    # ==========================================================================
    tools = []
    
    # Built-in Gemini tools
    tools.append(get_google_search_tool())
    tools.append(get_url_context_tool())
    
    # Vertex AI Search (if configured)
    if settings.vertex_search.data_store_id:
        tools.append(get_vertex_ai_search_tool())
    
    # Function tools (calculator, time, sentiment, etc.)
    tools.extend(get_sample_function_tools())
    
    # Memory tools (LoadArtifacts, LoadMemory, PreloadMemory)
    tools.extend(get_all_memory_tools())
    
    # ==========================================================================
    # USING MCP Integrations - Active MCP toolsets
    # ==========================================================================
    if include_mcp_tools:
        # GitHub MCP
        if os.getenv("GITHUB_TOKEN"):
            tools.append(get_github_mcp_toolset())
        # Notion MCP
        if os.getenv("NOTION_TOKEN"):
            tools.append(get_notion_mcp_toolset())
        # Stripe MCP
        if os.getenv("STRIPE_SECRET_KEY"):
            tools.append(get_stripe_mcp_toolset())
        # Hugging Face MCP
        if os.getenv("HF_TOKEN"):
            tools.append(get_huggingface_mcp_toolset())
        # ElevenLabs MCP
        if os.getenv("ELEVENLABS_API_KEY"):
            tools.append(get_elevenlabs_mcp_toolset())
        # PayPal MCP
        if os.getenv("PAYPAL_ACCESS_TOKEN") or os.getenv("PAYPAL_CLIENT_ID"):
            tools.append(get_paypal_mcp_toolset())
        # Linear MCP
        if os.getenv("LINEAR_API_KEY"):
            tools.append(get_linear_mcp_toolset())
        # Atlassian MCP
        if os.getenv("ATLASSIAN_API_TOKEN"):
            tools.append(get_atlassian_mcp_toolset())
        # Asana MCP
        if os.getenv("ASANA_ACCESS_TOKEN"):
            tools.append(get_asana_mcp_toolset())
        # GitLab MCP
        if os.getenv("GITLAB_TOKEN"):
            tools.append(get_gitlab_mcp_toolset())
        # Postman MCP
        if os.getenv("POSTMAN_API_KEY"):
            tools.append(get_postman_mcp_toolset())
        # N8N MCP
        if os.getenv("N8N_MCP_TOKEN") or os.getenv("N8N_API_KEY"):
            tools.append(get_n8n_mcp_toolset())
        # Daytona MCP
        if os.getenv("DAYTONA_API_KEY"):
            tools.append(get_daytona_mcp_toolset())
        # Cartesia MCP
        if os.getenv("CARTESIA_API_KEY"):
            tools.append(get_cartesia_mcp_toolset())
        # Chroma MCP (data_dir or Chroma Cloud env)
        if os.getenv("CHROMA_DATA_DIR") or os.getenv("CHROMA_API_KEY"):
            tools.append(get_chroma_mcp_toolset())
        # Qdrant MCP
        if os.getenv("QDRANT_URL"):
            tools.append(get_qdrant_mcp_toolset())
        # MongoDB MCP
        if os.getenv("MDB_MCP_CONNECTION_STRING"):
            tools.append(get_mongodb_mcp_toolset())
        # MCP Toolbox for Databases
        if os.getenv("TOOLBOX_SERVER_URL"):
            tools.append(get_toolbox_database_toolset())

    # ==========================================================================
    # USING Google Cloud toolsets (Pub/Sub, Bigtable, Spanner)
    # ==========================================================================
    if os.getenv("GOOGLE_CLOUD_PROJECT"):
        pubsub_ts = get_pubsub_toolset()
        if pubsub_ts is not None:
            tools.append(pubsub_ts)
        bigtable_ts = get_bigtable_toolset()
        if bigtable_ts is not None:
            tools.append(bigtable_ts)
        spanner_ts = get_spanner_toolset()
        if spanner_ts is not None:
            tools.append(spanner_ts)
    
    # ==========================================================================
    # USING Callbacks - Active callback functions
    # ==========================================================================
    callbacks = {}
    if use_all_callbacks:
        callbacks = {
            "before_agent_callback": sample_before_agent_callback,
            "after_agent_callback": sample_after_agent_callback,
            "before_tool_callback": sample_before_tool_callback,
            "after_tool_callback": sample_after_tool_callback,
            "before_model_callback": sample_before_model_callback,
            "after_model_callback": sample_after_model_callback,
        }
    
    # ==========================================================================
    # Create Agent with ALL capabilities actively used
    # ==========================================================================
    agent = LlmAgent(
        name="comprehensive_agent",
        model=model or DEFAULT_MODEL,
        description="Comprehensive agent with ALL plugins, services, and integrations actively used",
        instruction=COMPREHENSIVE_INSTRUCTION,
        tools=tools,
        # USING plugins
        plugins=plugins if plugins else None,
        # USING callbacks
        **callbacks,
    )
    
    return agent


# =============================================================================
# Pre-configured Comprehensive Agent Instance
# =============================================================================

# Direct instantiation showing all capabilities are USED
comprehensive_agent = LlmAgent(
    name="comprehensive_agent",
    model="gemini-2.5-flash",  # Direct model string
    description="Agent that actively USES all plugins, services, and integrations",
    instruction=COMPREHENSIVE_INSTRUCTION,
    tools=[
        # Built-in tools - USED
        get_google_search_tool(),
        get_url_context_tool(),
        # Function tools - USED
        *get_sample_function_tools(),
        # Memory tools - USED
        *get_all_memory_tools(),
    ],
    # Plugins - USED
    plugins=[
        logging_plugin,        # LoggingPlugin instance
        debug_logging_plugin,  # DebugLoggingPlugin instance
        retry_plugin,          # ReflectAndRetryToolPlugin instance
    ],
    # Callbacks - USED
    before_agent_callback=sample_before_agent_callback,
    after_agent_callback=sample_after_agent_callback,
    before_tool_callback=sample_before_tool_callback,
    after_tool_callback=sample_after_tool_callback,
    before_model_callback=sample_before_model_callback,
    after_model_callback=sample_after_model_callback,
)
