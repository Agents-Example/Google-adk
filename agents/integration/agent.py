"""
Integration agent - specialized for Google API integrations.

This agent demonstrates:
- Multiple Google API toolsets (Calendar, Gmail, Docs, Sheets, Slides, YouTube)
- OAuth authentication handling
- Tool filtering for specific operations
- Enterprise integrations (APIHub, Application Integration)
"""

from typing import Optional, List

from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import (
    CalendarToolset,
    GmailToolset,
    DocsToolset,
    SheetsToolset,
    SlidesToolset,
    YoutubeToolset,
)
from google.adk.tools.base_toolset import BaseToolset

from config.constants import (
    INTEGRATION_AGENT_NAME,
    INTEGRATION_INSTRUCTION,
    AGENT_DESCRIPTIONS,
)
from config.settings import get_settings
from services.credential import get_oauth_credentials
from tools.google_api_tools import (
    get_calendar_toolset,
    get_gmail_toolset,
    get_docs_toolset,
    get_sheets_toolset,
    get_slides_toolset,
    get_youtube_toolset,
    get_all_google_api_toolsets,
)
from tools.enterprise_tools import (
    get_apihub_toolset,
    get_application_integration_toolset,
)


def create_integration_agent(
    model: Optional[str] = None,
    services: Optional[List[str]] = None,
    include_enterprise: bool = False,
) -> LlmAgent:
    """
    Create the integration agent.
    
    The integration agent manages connections to various Google APIs
    and enterprise integration platforms.
    
    Args:
        model: Model to use. Defaults to settings.
        services: List of services to include. If None, includes all.
                 Options: calendar, gmail, docs, sheets, slides, youtube
        include_enterprise: Include enterprise integrations (APIHub, etc.)
    
    Returns:
        LlmAgent: The configured integration agent.
    
    Example:
        # All integrations
        integration = create_integration_agent()
        
        # Specific services only
        integration = create_integration_agent(
            services=["calendar", "gmail"]
        )
        
        # With enterprise integrations
        integration = create_integration_agent(include_enterprise=True)
    """
    settings = get_settings()
    
    # Service mapping
    service_getters = {
        "calendar": get_calendar_toolset,
        "gmail": get_gmail_toolset,
        "docs": get_docs_toolset,
        "sheets": get_sheets_toolset,
        "slides": get_slides_toolset,
        "youtube": get_youtube_toolset,
    }
    
    # Build tools list
    tools: List[BaseToolset] = []
    
    if services:
        # Add specific services
        for service in services:
            if service in service_getters:
                tools.append(service_getters[service]())
    else:
        # Add all services
        tools.extend(get_all_google_api_toolsets())
    
    # Add enterprise integrations if requested
    if include_enterprise:
        if settings.api_hub.resource_name:
            try:
                tools.append(get_apihub_toolset())
            except Exception:
                pass
        
        if settings.app_integration.project:
            try:
                tools.append(get_application_integration_toolset())
            except Exception:
                pass
    
    return LlmAgent(
        name=INTEGRATION_AGENT_NAME,
        model=model or settings.models.default_model,
        description=AGENT_DESCRIPTIONS[INTEGRATION_AGENT_NAME],
        instruction=INTEGRATION_INSTRUCTION,  # From constants
        tools=tools,
        disallow_transfer_to_parent=False,
    )


# Pre-configured integration agent
# Demonstrates direct toolset instantiation with OAuth credentials
client_id, client_secret = get_oauth_credentials()

integration_agent = LlmAgent(
    name=INTEGRATION_AGENT_NAME,
    model="gemini-2.5-flash",  # Direct string
    description="Manages integrations with Google APIs including Calendar, Gmail, Docs, Sheets, Slides, and YouTube.",
    instruction="""You are a Google API integration specialist.

Your capabilities span multiple Google services:

Calendar:
- Create, read, update, delete calendar events
- Manage multiple calendars
- Set up reminders and notifications

Gmail:
- Read and search emails
- Send emails and replies
- Manage labels and threads

Google Docs:
- Create new documents
- Edit existing documents
- Export and format documents

Google Sheets:
- Read and write spreadsheet data
- Manage multiple sheets
- Perform calculations and formulas

Google Slides:
- Create presentations
- Add and edit slides
- Insert text, images, and shapes

YouTube:
- Search for videos
- Get video information
- Manage playlists

Guidelines:
1. Always confirm before making changes (especially deletes)
2. Handle authentication prompts appropriately
3. Respect rate limits and quotas
4. Provide clear feedback on operation results
5. Ask for clarification on ambiguous requests

OAuth Note:
Some operations require user authentication. If prompted,
guide the user through the OAuth flow.
""",  # Direct instruction
    tools=[
        CalendarToolset(client_id=client_id, client_secret=client_secret),
        GmailToolset(client_id=client_id, client_secret=client_secret),
        DocsToolset(client_id=client_id, client_secret=client_secret),
        SheetsToolset(client_id=client_id, client_secret=client_secret),
        SlidesToolset(client_id=client_id, client_secret=client_secret),
        YoutubeToolset(client_id=client_id, client_secret=client_secret),
    ],  # Direct toolset instantiation
)
