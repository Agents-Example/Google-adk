"""
UI integrations for Google ADK.

Provides configurations for UI frameworks:
- AG-UI: Open protocol for rich agent UIs
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


# =============================================================================
# AG-UI Integration
# =============================================================================

@dataclass
class AGUIConfig:
    """
    Configuration for AG-UI integration.
    
    AG-UI is an open protocol for building interactive chat UIs with:
    - Streaming events
    - Client state synchronization
    - Bi-directional communication
    
    Compatible clients:
    - CopilotKit (React)
    - Kotlin, Java, Go SDKs
    - CLI implementations
    """
    frontend_port: int = 3000
    backend_port: int = 8000


ag_ui_config = AGUIConfig()


def setup_ag_ui(
    frontend_port: int = 3000,
    backend_port: int = 8000,
) -> Dict[str, Any]:
    """
    Setup AG-UI for rich agent UIs.
    
    AG-UI enables interactive chat UIs with streaming, state sync,
    and generative UI capabilities.
    
    Args:
        frontend_port: Port for the web UI.
        backend_port: Port for the ADK agent API.
    
    Returns:
        Dict: Configuration for AG-UI setup.
    
    Quickstart:
        # Create app
        npx copilotkit@latest create -f adk
        
        # Set API key
        export GOOGLE_API_KEY="your-api-key"
        
        # Run
        npm install && npm run dev
    
    Features:
        - Chat: Streaming messages between users and agents
        - Generative UI: Display tool outputs as React components
        - Shared State: Synchronize state between agent and UI
    
    Example CopilotKit usage:
        ```tsx
        // Chat sidebar
        <CopilotSidebar
            defaultOpen={true}
            labels={{ title: "AI Assistant" }}
        />
        
        // Render tool calls as UI
        useRenderToolCall({
            name: "get_weather",
            render: ({ args }) => <WeatherCard location={args.location} />
        })
        
        // Shared state
        const { state, setState } = useCoAgent<AgentState>({
            name: "my_agent",
            initialState: { items: [] }
        })
        ```
    """
    return {
        "frontend_port": frontend_port,
        "backend_port": backend_port,
        "frontend_url": f"http://localhost:{frontend_port}",
        "backend_url": f"http://localhost:{backend_port}",
        "setup_command": "npx copilotkit@latest create -f adk",
    }
