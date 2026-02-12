"""
Google API toolsets for Google ADK.

This module provides toolsets for various Google APIs including:
- CalendarToolset: Google Calendar
- GmailToolset: Gmail
- DocsToolset: Google Docs
- SheetsToolset: Google Sheets
- SlidesToolset: Google Slides
- YoutubeToolset: YouTube
- BigQueryToolset: BigQuery (auto-generated)

These toolsets are auto-generated based on Google API Discovery API
specifications and require OAuth2 authentication.
"""

from typing import Optional, List

from google.adk.tools.google_api_tool import (
    GoogleApiToolset,
    CalendarToolset,
    GmailToolset,
    DocsToolset,
    SheetsToolset,
    SlidesToolset,
    YoutubeToolset,
    BigQueryToolset,
)
from google.adk.tools.bigquery import (
    BigQueryToolset as CustomBigQueryToolset,
    BigQueryCredentialsConfig,
)
from google.adk.tools.base_toolset import BaseToolset, ToolPredicate

from config.settings import get_settings
from services.credential import get_oauth_credentials


def get_calendar_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> CalendarToolset:
    """
    Create a Google Calendar toolset.
    
    Provides tools for Google Calendar operations including:
    - Creating, reading, updating, deleting events
    - Managing calendars and calendar lists
    - Handling event reminders and notifications
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
    
    Returns:
        CalendarToolset: A configured Calendar toolset.
    
    Example:
        # With default credentials
        calendar = get_calendar_toolset()
        
        # With specific tools
        calendar = get_calendar_toolset(
            tool_filter=["calendar_events_list", "calendar_events_insert"]
        )
    """
    # Use environment credentials if not provided
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return CalendarToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
    )


def get_gmail_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> GmailToolset:
    """
    Create a Gmail toolset.
    
    Provides tools for Gmail operations including:
    - Reading and sending emails
    - Managing labels and threads
    - Searching messages
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
    
    Returns:
        GmailToolset: A configured Gmail toolset.
    
    Example:
        gmail = get_gmail_toolset()
        # Or with filtered tools
        gmail = get_gmail_toolset(
            tool_filter=["gmail_users_messages_list", "gmail_users_messages_send"]
        )
    """
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return GmailToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
    )


def get_docs_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> DocsToolset:
    """
    Create a Google Docs toolset.
    
    Provides tools for Google Docs operations including:
    - Creating and editing documents
    - Batch updates
    - Reading document content
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
    
    Returns:
        DocsToolset: A configured Docs toolset.
    """
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return DocsToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
    )


def get_sheets_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> SheetsToolset:
    """
    Create a Google Sheets toolset.
    
    Provides tools for Google Sheets operations including:
    - Reading and writing spreadsheet data
    - Managing sheets and ranges
    - Batch updates
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
    
    Returns:
        SheetsToolset: A configured Sheets toolset.
    """
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return SheetsToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
    )


def get_slides_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> SlidesToolset:
    """
    Create a Google Slides toolset.
    
    Provides tools for Google Slides operations including:
    - Creating presentations
    - Adding and editing slides
    - Managing slide content
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
    
    Returns:
        SlidesToolset: A configured Slides toolset.
    """
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return SlidesToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
    )


def get_youtube_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
) -> YoutubeToolset:
    """
    Create a YouTube toolset.
    
    Provides tools for YouTube operations including:
    - Searching videos
    - Retrieving video information
    - Managing playlists
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
    
    Returns:
        YoutubeToolset: A configured YouTube toolset.
    """
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return YoutubeToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
    )


def get_bigquery_toolset(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tool_filter: Optional[List[str] | ToolPredicate] = None,
    use_custom: bool = False,
) -> BaseToolset:
    """
    Create a BigQuery toolset.
    
    Can create either the auto-generated BigQuery toolset or the
    custom BigQuery toolset with hand-crafted tools.
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
        tool_filter: Optional filter to include only specific tools.
        use_custom: If True, use the custom BigQuery toolset.
    
    Returns:
        BaseToolset: A configured BigQuery toolset.
    
    Example:
        # Auto-generated toolset
        bq = get_bigquery_toolset()
        
        # Custom toolset with hand-crafted tools
        bq = get_bigquery_toolset(use_custom=True)
    """
    if use_custom:
        # Custom BigQuery toolset with hand-crafted tools
        return CustomBigQueryToolset(
            tool_filter=tool_filter,
            credentials_config=BigQueryCredentialsConfig(),
        )
    else:
        # Auto-generated from API spec
        if client_id is None or client_secret is None:
            env_client_id, env_client_secret = get_oauth_credentials()
            client_id = client_id or env_client_id
            client_secret = client_secret or env_client_secret
        
        return BigQueryToolset(
            client_id=client_id,
            client_secret=client_secret,
            tool_filter=tool_filter,
        )


def get_all_google_api_toolsets(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> List[BaseToolset]:
    """
    Get all Google API toolsets.
    
    Returns a list of all available Google API toolsets configured
    with the provided or default credentials.
    
    Args:
        client_id: OAuth2 client ID. Defaults to settings.
        client_secret: OAuth2 client secret. Defaults to settings.
    
    Returns:
        List[BaseToolset]: List of all Google API toolsets.
    
    Example:
        toolsets = get_all_google_api_toolsets()
        agent = LlmAgent(
            name="google_integration",
            tools=toolsets  # Pass list of toolsets
        )
    """
    if client_id is None or client_secret is None:
        env_client_id, env_client_secret = get_oauth_credentials()
        client_id = client_id or env_client_id
        client_secret = client_secret or env_client_secret
    
    return [
        get_calendar_toolset(client_id, client_secret),
        get_gmail_toolset(client_id, client_secret),
        get_docs_toolset(client_id, client_secret),
        get_sheets_toolset(client_id, client_secret),
        get_slides_toolset(client_id, client_secret),
        get_youtube_toolset(client_id, client_secret),
        get_bigquery_toolset(client_id, client_secret),
    ]


# Pre-configured toolset instances for direct use
# Using inline definitions (as requested for variety in style)

settings = get_settings()
_client_id, _client_secret = get_oauth_credentials()

# Direct instantiation style (alternative to factory functions)
calendar_toolset = CalendarToolset(
    client_id=_client_id,
    client_secret=_client_secret,
)

gmail_toolset = GmailToolset(
    client_id=_client_id,
    client_secret=_client_secret,
)

docs_toolset = DocsToolset(
    client_id=_client_id,
    client_secret=_client_secret,
)

sheets_toolset = SheetsToolset(
    client_id=_client_id,
    client_secret=_client_secret,
)

slides_toolset = SlidesToolset(
    client_id=_client_id,
    client_secret=_client_secret,
)

youtube_toolset = YoutubeToolset(
    client_id=_client_id,
    client_secret=_client_secret,
)
