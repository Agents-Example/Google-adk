"""
MCP Hub Agent - Uses ALL MCP integrations.

This agent demonstrates every MCP integration documented in Google ADK:
- GitHub, Hugging Face, Notion, Stripe, ElevenLabs
- PayPal, Linear, Atlassian, Asana, GitLab
- Postman, N8N, Daytona
- MCP Toolbox for Databases
"""

from typing import Optional, List
import os

from google.adk.agents import LlmAgent

from integrations.mcp_integrations import (
    # Code & DevOps
    get_github_mcp_toolset,
    get_gitlab_mcp_toolset,
    get_daytona_mcp_toolset,
    # AI & ML
    get_huggingface_mcp_toolset,
    get_elevenlabs_mcp_toolset,
    # Productivity
    get_notion_mcp_toolset,
    get_linear_mcp_toolset,
    get_atlassian_mcp_toolset,
    get_asana_mcp_toolset,
    # Business & Payments
    get_stripe_mcp_toolset,
    get_paypal_mcp_toolset,
    # API & Automation
    get_postman_mcp_toolset,
    get_n8n_mcp_toolset,
)

from integrations.database_integrations import (
    get_toolbox_database_toolset,
)

from config import DEFAULT_MODEL


MCP_HUB_INSTRUCTION = """You are the MCP Hub Agent with access to ALL Model Context Protocol integrations.

Your MCP capabilities include:

**Code & DevOps:**
- GitHub: Repository management, issues, PRs, actions, code security
- GitLab: Code management, CI/CD, merge requests
- Daytona: Development environment management

**AI & ML:**
- Hugging Face: Models, datasets, papers, Gradio apps
- ElevenLabs: Text-to-speech, voice cloning, audio processing

**Productivity:**
- Notion: Workspace search, page management, databases
- Linear: Issue tracking, project management
- Atlassian: Jira issues, Confluence pages
- Asana: Task management, project tracking

**Business & Payments:**
- Stripe: Payments, customers, subscriptions, invoices
- PayPal: Payment processing, transactions

**API & Automation:**
- Postman: API testing, collections, environments
- N8N: Workflow automation, integrations

**Databases:**
- MCP Toolbox: 30+ database connections (BigQuery, PostgreSQL, MongoDB, Neo4j, etc.)

Use the appropriate MCP tool for each request. If credentials are not configured,
explain which environment variable needs to be set.
"""


def create_mcp_hub_agent(
    model: Optional[str] = None,
    include_all_integrations: bool = True,
) -> LlmAgent:
    """
    Create MCP Hub Agent with ALL MCP integrations.
    
    Args:
        model: LLM model to use.
        include_all_integrations: Include all MCP tools (if env vars set).
    
    Returns:
        LlmAgent: Configured MCP hub agent.
    """
    tools = []
    
    if include_all_integrations:
        # Code & DevOps
        if os.getenv("GITHUB_TOKEN"):
            tools.append(get_github_mcp_toolset())
        if os.getenv("GITLAB_TOKEN"):
            tools.append(get_gitlab_mcp_toolset())
        if os.getenv("DAYTONA_API_KEY"):
            tools.append(get_daytona_mcp_toolset())
        
        # AI & ML
        if os.getenv("HF_TOKEN"):
            tools.append(get_huggingface_mcp_toolset())
        if os.getenv("ELEVENLABS_API_KEY"):
            tools.append(get_elevenlabs_mcp_toolset())
        
        # Productivity
        if os.getenv("NOTION_TOKEN"):
            tools.append(get_notion_mcp_toolset())
        if os.getenv("LINEAR_API_KEY"):
            tools.append(get_linear_mcp_toolset())
        if os.getenv("ATLASSIAN_API_TOKEN"):
            tools.append(get_atlassian_mcp_toolset())
        if os.getenv("ASANA_ACCESS_TOKEN"):
            tools.append(get_asana_mcp_toolset())
        
        # Business & Payments
        if os.getenv("STRIPE_SECRET_KEY"):
            tools.append(get_stripe_mcp_toolset())
        if os.getenv("PAYPAL_CLIENT_ID"):
            tools.append(get_paypal_mcp_toolset())
        
        # API & Automation
        if os.getenv("POSTMAN_API_KEY"):
            tools.append(get_postman_mcp_toolset())
        if os.getenv("N8N_API_KEY"):
            tools.append(get_n8n_mcp_toolset())
        
        # Databases
        if os.getenv("TOOLBOX_SERVER_URL"):
            tools.append(get_toolbox_database_toolset())
    
    return LlmAgent(
        name="mcp_hub_agent",
        model=model or DEFAULT_MODEL,
        description="MCP Hub with ALL MCP integrations",
        instruction=MCP_HUB_INSTRUCTION,
        tools=tools,
    )


# Pre-configured instance (tools added when env vars are set)
mcp_hub_agent = create_mcp_hub_agent()
