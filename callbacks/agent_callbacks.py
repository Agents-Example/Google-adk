"""
Agent callbacks for Google ADK.

Agent callbacks are invoked before and after agent execution.
They can be used for:
- Logging and monitoring
- State modification
- Response modification
- Error handling
"""

from typing import Optional
import logging

from google.adk.agents.callback_context import CallbackContext
from google.genai.types import Content

logger = logging.getLogger(__name__)


def sample_before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """
    Sample before-agent callback.
    
    This callback is invoked before the agent starts processing.
    It can be used to:
    - Log agent invocation
    - Modify input state
    - Short-circuit execution by returning Content
    
    Args:
        callback_context: Context with agent and invocation info.
    
    Returns:
        Optional[Content]: Return Content to skip agent execution,
                          or None to continue normally.
    
    Example:
        agent = LlmAgent(
            name="my_agent",
            before_agent_callback=sample_before_agent_callback
        )
    """
    agent = callback_context.agent
    state = callback_context.state
    
    logger.info(f"Before agent '{agent.name}' - State: {state}")
    
    # Return None to continue with normal agent execution
    return None


def sample_after_agent_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """
    Sample after-agent callback.
    
    This callback is invoked after the agent completes processing.
    It can be used to:
    - Log agent completion
    - Post-process the response
    - Modify or replace the response
    
    Args:
        callback_context: Context with agent and result info.
    
    Returns:
        Optional[Content]: Return Content to replace agent response,
                          or None to use the original response.
    
    Example:
        agent = LlmAgent(
            name="my_agent",
            after_agent_callback=sample_after_agent_callback
        )
    """
    agent = callback_context.agent
    state = callback_context.state
    
    logger.info(f"After agent '{agent.name}' - State: {state}")
    
    # Return None to keep the original response
    return None


def logging_before_agent(callback_context: CallbackContext) -> Optional[Content]:
    """
    Logging callback for agent start.
    
    Logs detailed information about agent invocation.
    """
    agent = callback_context.agent
    state = callback_context.state
    invocation_id = callback_context.invocation_id
    
    logger.info(
        f"[AGENT START] Agent: {agent.name} | "
        f"Invocation: {invocation_id} | "
        f"State keys: {list(state.keys()) if hasattr(state, 'keys') else 'N/A'}"
    )
    
    return None


def logging_after_agent(callback_context: CallbackContext) -> Optional[Content]:
    """
    Logging callback for agent completion.
    
    Logs completion information and timing.
    """
    agent = callback_context.agent
    invocation_id = callback_context.invocation_id
    
    logger.info(
        f"[AGENT END] Agent: {agent.name} | "
        f"Invocation: {invocation_id}"
    )
    
    return None


def state_modification_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """
    Example callback that modifies state.
    
    Demonstrates how to modify agent state in callbacks.
    """
    # Access state through actions
    actions = callback_context.actions
    
    # Track invocation count in state
    current_count = callback_context.state.get("invocation_count", 0)
    actions.state_delta["invocation_count"] = current_count + 1
    
    return None


def error_handling_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """
    Example callback for error handling.
    
    Can be used to catch errors and provide fallback responses.
    """
    from google.genai.types import Content, Part
    
    # Check if there was an error (would be in after callback)
    error = callback_context.state.get("_error")
    
    if error:
        # Return a fallback response
        return Content(parts=[
            Part(text=f"An error occurred: {error}. Please try again.")
        ])
    
    return None


"""
Agent Callback Patterns
=======================

1. Logging/Monitoring
---------------------
agent = LlmAgent(
    name="monitored_agent",
    before_agent_callback=logging_before_agent,
    after_agent_callback=logging_after_agent
)

2. State Modification
---------------------
agent = LlmAgent(
    name="stateful_agent",
    before_agent_callback=state_modification_callback
)

3. Short-Circuit Execution
--------------------------
def auth_check_callback(ctx):
    if not ctx.state.get("authenticated"):
        from google.genai.types import Content, Part
        return Content(parts=[Part(text="Please authenticate first.")])
    return None

agent = LlmAgent(
    name="secure_agent",
    before_agent_callback=auth_check_callback
)

4. Response Post-Processing
---------------------------
def format_response_callback(ctx):
    # Access original response through context
    # Modify and return new content if needed
    return None  # Or return modified Content

agent = LlmAgent(
    name="formatted_agent",
    after_agent_callback=format_response_callback
)
"""
