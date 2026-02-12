"""
Code executor integrations for Google ADK.

Provides configurations for code execution:
- Computer Use (Playwright-based browser automation)
- GKE Code Executor (Kubernetes-based execution)
"""

import os
from typing import Optional, Tuple
from dataclasses import dataclass

from google.adk.tools.computer_use.computer_use_toolset import ComputerUseToolset


# =============================================================================
# Computer Use (Browser Automation)
# =============================================================================

@dataclass
class ComputerUseConfig:
    """
    Configuration for Computer Use toolset.
    
    Computer Use allows agents to operate browser interfaces using
    Gemini models and Playwright for Chromium control.
    
    Capabilities:
    - Take screenshots
    - Click elements
    - Type text
    - Navigate pages
    """
    screen_size: Tuple[int, int] = (1280, 936)
    model: str = "gemini-2.5-computer-use-preview-10-2025"
    headless: bool = True


computer_use_config = ComputerUseConfig()


def get_computer_use_toolset(
    screen_size: Tuple[int, int] = (1280, 936),
) -> ComputerUseToolset:
    """
    Get Computer Use toolset for browser automation.
    
    Computer Use enables agents to interact with web interfaces
    using the Playwright testing tool and Chromium browser.
    
    Args:
        screen_size: Browser viewport size (width, height).
    
    Returns:
        ComputerUseToolset: Configured toolset.
    
    Prerequisites:
        pip install playwright termcolor rich
        playwright install-deps chromium
        playwright install chromium
    
    Example:
        from google.adk import Agent
        from integrations.code_executors import get_computer_use_toolset
        
        agent = Agent(
            model='gemini-2.5-computer-use-preview-10-2025',
            name='browser_agent',
            tools=[get_computer_use_toolset()],
        )
    
    Note:
        Requires PlaywrightComputer implementation for BaseComputer.
        See the computer_use sample for complete implementation.
    """
    # Note: This requires a BaseComputer implementation
    # In production, you would provide PlaywrightComputer
    # from your implementation
    
    class MockComputer:
        """Mock computer for structural demonstration."""
        def __init__(self, screen_size):
            self.screen_size = screen_size
    
    # Return toolset with mock computer for structure
    # Real implementation requires PlaywrightComputer
    return ComputerUseToolset(
        computer=MockComputer(screen_size=screen_size)
    )


# =============================================================================
# GKE Code Executor
# =============================================================================

@dataclass
class GKEExecutorConfig:
    """
    Configuration for GKE-based code execution.
    
    GKE Code Executor provides secure, containerized code execution
    in a Kubernetes environment.
    """
    project: Optional[str] = None
    location: str = "us-central1"
    cluster_name: Optional[str] = None
    namespace: str = "default"
    image: str = "python:3.11-slim"
    timeout_seconds: int = 300
    
    def __post_init__(self):
        self.project = self.project or os.getenv("GOOGLE_CLOUD_PROJECT")


def get_gke_executor_config(
    project: Optional[str] = None,
    cluster_name: Optional[str] = None,
    namespace: str = "default",
    image: str = "python:3.11-slim",
) -> GKEExecutorConfig:
    """
    Get GKE Code Executor configuration.
    
    GKE provides secure, containerized code execution for agents.
    
    Args:
        project: GCP project ID.
        cluster_name: GKE cluster name.
        namespace: Kubernetes namespace.
        image: Docker image for execution.
    
    Returns:
        GKEExecutorConfig: Configuration object.
    
    Usage:
        config = get_gke_executor_config(
            cluster_name="my-cluster",
            namespace="code-execution"
        )
    """
    return GKEExecutorConfig(
        project=project,
        cluster_name=cluster_name,
        namespace=namespace,
        image=image,
    )
