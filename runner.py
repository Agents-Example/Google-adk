"""
Runner configuration for Google ADK Multi-Agent System.

The Runner provides programmatic access to agent execution without
a web interface. It's the core execution engine.

Demonstrates:
- Runner with custom services
- InMemoryRunner for quick testing
- RunConfig for execution settings
- LiveRequest and LiveRequestQueue for streaming
"""

from typing import Optional, AsyncIterator

from google.adk import Runner, InMemoryRunner
from google.adk.agents import LlmAgent, InvocationContext, LiveRequest, LiveRequestQueue
from google.adk.runners import RunConfig, StreamingMode
from google.adk.sessions import BaseSessionService, Session
from google.adk.artifacts import BaseArtifactService
from google.adk.memory import BaseMemoryService
from google.adk.events import Event

from config.settings import get_settings
from config.constants import DEFAULT_MAX_LLM_CALLS
from services.session import create_session_service
from services.artifact import create_artifact_service
from services.memory import create_memory_service
from agents.orchestrator.agent import build_multi_agent_system


def create_runner(
    agent: Optional[LlmAgent] = None,
    session_service: Optional[BaseSessionService] = None,
    artifact_service: Optional[BaseArtifactService] = None,
    memory_service: Optional[BaseMemoryService] = None,
    credential_service=None,
) -> Runner:
    """
    Create a configured Runner instance.
    
    The Runner executes agents programmatically without a web interface.
    It manages sessions, artifacts, and memory.
    
    Args:
        agent: The root agent. Defaults to full multi-agent system.
        session_service: Session service. Defaults to InMemory.
        artifact_service: Artifact service. Defaults to InMemory.
        memory_service: Memory service. Defaults to InMemory.
        credential_service: Optional credential service.
    
    Returns:
        Runner: A configured Runner instance.
    
    Example:
        runner = create_runner()
        
        async for event in runner.run_async(
            user_id="user123",
            session_id="session456",
            new_message="Hello!"
        ):
            print(event)
    """
    # Create default services if not provided
    if session_service is None:
        session_service = create_session_service()
    
    if artifact_service is None:
        artifact_service = create_artifact_service("inmemory")
    
    if memory_service is None:
        memory_service = create_memory_service("inmemory")
    
    # Create default agent if not provided
    if agent is None:
        agent = build_multi_agent_system()
    
    return Runner(
        agent=agent,
        session_service=session_service,
        artifact_service=artifact_service,
        memory_service=memory_service,
        credential_service=credential_service,
    )


def create_inmemory_runner(agent: Optional[LlmAgent] = None) -> InMemoryRunner:
    """
    Create an InMemoryRunner for quick testing.
    
    InMemoryRunner uses in-memory services for all storage,
    making it ideal for testing and development.
    
    Args:
        agent: The agent to use. Defaults to full multi-agent system.
    
    Returns:
        InMemoryRunner: A configured InMemoryRunner.
    
    Example:
        runner = create_inmemory_runner()
        response = await runner.run("What is 2+2?")
    """
    if agent is None:
        agent = build_multi_agent_system()
    
    return InMemoryRunner(agent=agent)


def create_run_config(
    max_llm_calls: int = DEFAULT_MAX_LLM_CALLS,
    streaming_mode: str = "NONE",
    save_input_blobs: bool = True,
    support_cfc: bool = False,
) -> RunConfig:
    """
    Create a RunConfig for execution settings.
    
    RunConfig controls how the agent executes, including
    limits, streaming, and feature flags.
    
    Args:
        max_llm_calls: Maximum LLM calls per run.
        streaming_mode: "NONE", "SSE", or "BIDI".
        save_input_blobs: Save input blobs to artifacts.
        support_cfc: Support Compositional Function Calling.
    
    Returns:
        RunConfig: A configured RunConfig.
    
    Example:
        config = create_run_config(max_llm_calls=100)
        
        async for event in runner.run_async(
            ...,
            run_config=config
        ):
            ...
    """
    # Map streaming mode string to enum
    streaming_enum = getattr(StreamingMode, streaming_mode, StreamingMode.NONE)
    
    return RunConfig(
        max_llm_calls=max_llm_calls,
        streaming_mode=streaming_enum,
        save_input_blobs_as_artifacts=save_input_blobs,
        support_cfc=support_cfc,
    )


async def run_agent(
    runner: Runner,
    user_id: str,
    message: str,
    session_id: Optional[str] = None,
    run_config: Optional[RunConfig] = None,
) -> AsyncIterator[Event]:
    """
    Run an agent with a message.
    
    Convenience function for running agents asynchronously.
    
    Args:
        runner: The Runner instance.
        user_id: User identifier.
        message: The user's message.
        session_id: Optional session ID for continuity.
        run_config: Optional run configuration.
    
    Yields:
        Event: Events from the agent execution.
    
    Example:
        runner = create_runner()
        
        async for event in run_agent(
            runner,
            user_id="user123",
            message="Search for Python tutorials"
        ):
            print(event)
    """
    # Create or get session
    session_service = runner.session_service
    app_name = runner.agent.name
    
    if session_id:
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
    else:
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
        )
    
    # Run agent
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=message,
        run_config=run_config,
    ):
        yield event


def create_live_request_queue() -> LiveRequestQueue:
    """
    Create a LiveRequestQueue for streaming interactions.
    
    LiveRequestQueue enables real-time streaming of requests
    and responses for interactive applications.
    
    Returns:
        LiveRequestQueue: A new request queue.
    
    Example:
        queue = create_live_request_queue()
        queue.send(LiveRequest(content=user_message))
        
        async for response in queue.receive():
            process(response)
    """
    return LiveRequestQueue()


# Pre-configured Runner instances

# Development runner with InMemory services
settings = get_settings()

# Using factory functions
dev_runner = create_runner(
    agent=build_multi_agent_system(),
    session_service=create_session_service(use_vertex=False),
    artifact_service=create_artifact_service("inmemory"),
    memory_service=create_memory_service("inmemory"),
)

# Quick test runner
test_runner = InMemoryRunner(
    agent=build_multi_agent_system()
)

# Default run config
default_run_config = RunConfig(
    max_llm_calls=DEFAULT_MAX_LLM_CALLS,  # From constant
    streaming_mode=StreamingMode.NONE,
    save_input_blobs_as_artifacts=True,
)


"""
Runner Usage Patterns
=====================

1. Basic Execution
------------------
runner = create_runner()

async def chat(message):
    async for event in runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=message
    ):
        if event.type == "content":
            print(event.content)

2. InMemory Testing
-------------------
runner = create_inmemory_runner()
response = await runner.run("What is 2+2?")

3. With Run Config
------------------
runner = create_runner()
config = create_run_config(max_llm_calls=50)

async for event in runner.run_async(
    user_id="user1",
    session_id="session1",
    new_message="Complex task...",
    run_config=config
):
    ...

4. Live Streaming
-----------------
queue = create_live_request_queue()

# Send requests
queue.send(LiveRequest(content="Hello"))

# Receive responses
async for response in queue.receive():
    print(response)

5. Session Continuity
---------------------
runner = create_runner()

# First interaction
session_id = None
async for event in runner.run_async(
    user_id="user1",
    session_id=session_id,
    new_message="Remember my name is Alice"
):
    if event.type == "session_created":
        session_id = event.session_id

# Second interaction (same session)
async for event in runner.run_async(
    user_id="user1",
    session_id=session_id,  # Reuse session
    new_message="What is my name?"
):
    ...
"""
