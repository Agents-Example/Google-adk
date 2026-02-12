"""
Model callbacks for Google ADK.

Model callbacks are invoked before and after LLM calls.
They can be used for:
- Logging model interactions
- Modifying prompts
- Token tracking
- Rate limiting
"""

from typing import Optional, List
import logging

from google.adk.agents.callback_context import CallbackContext
from google.genai.types import Content

logger = logging.getLogger(__name__)


def sample_before_model_callback(
    callback_context: CallbackContext,
    llm_request: List[Content],
) -> Optional[List[Content]]:
    """
    Sample before-model callback.
    
    This callback is invoked before sending a request to the LLM.
    It can be used to:
    - Log model requests
    - Modify the prompt
    - Add system context
    - Implement rate limiting
    
    Args:
        callback_context: Context with model call info.
        llm_request: The content being sent to the model.
    
    Returns:
        Optional[List[Content]]: Modified request, or None to use original.
    
    Example:
        agent = LlmAgent(
            name="my_agent",
            before_model_callback=sample_before_model_callback
        )
    """
    logger.info(f"Before model call - Request parts: {len(llm_request)}")
    
    # Return None to use original request
    return None


def sample_after_model_callback(
    callback_context: CallbackContext,
    llm_response: Content,
) -> Optional[Content]:
    """
    Sample after-model callback.
    
    This callback is invoked after receiving a response from the LLM.
    It can be used to:
    - Log model responses
    - Post-process output
    - Track token usage
    - Filter sensitive content
    
    Args:
        callback_context: Context with model call info.
        llm_response: The response from the model.
    
    Returns:
        Optional[Content]: Modified response, or None to use original.
    
    Example:
        agent = LlmAgent(
            name="my_agent",
            after_model_callback=sample_after_model_callback
        )
    """
    # Log response
    parts_count = len(llm_response.parts) if llm_response.parts else 0
    logger.info(f"After model call - Response parts: {parts_count}")
    
    # Return None to use original response
    return None


def model_logging_callback(
    callback_context: CallbackContext,
    llm_request: List[Content],
) -> Optional[List[Content]]:
    """
    Comprehensive logging callback for model calls.
    """
    agent = callback_context.agent
    invocation_id = callback_context.invocation_id
    
    # Calculate approximate token count (very rough estimate)
    total_chars = sum(
        len(str(part)) for content in llm_request for part in content.parts
    ) if llm_request else 0
    approx_tokens = total_chars // 4  # Rough estimate
    
    logger.info(
        f"[MODEL REQUEST] Agent: {agent.name} | "
        f"Invocation: {invocation_id} | "
        f"Messages: {len(llm_request)} | "
        f"~Tokens: {approx_tokens}"
    )
    
    return None


def rate_limit_callback(
    callback_context: CallbackContext,
    llm_request: List[Content],
) -> Optional[List[Content]]:
    """
    Rate limiting callback example.
    
    Tracks request count and can block if limit exceeded.
    """
    import time
    
    state = callback_context.state
    actions = callback_context.actions
    
    # Track requests
    request_count = state.get("_model_request_count", 0)
    last_request_time = state.get("_last_request_time", 0)
    current_time = time.time()
    
    # Reset counter if more than 1 minute passed
    if current_time - last_request_time > 60:
        request_count = 0
    
    # Update state
    actions.state_delta["_model_request_count"] = request_count + 1
    actions.state_delta["_last_request_time"] = current_time
    
    # Check rate limit (e.g., 100 requests per minute)
    if request_count > 100:
        logger.warning("Rate limit exceeded")
        # Could return a modified request or raise an exception
    
    return None


def context_injection_callback(
    callback_context: CallbackContext,
    llm_request: List[Content],
) -> Optional[List[Content]]:
    """
    Inject additional context into model requests.
    """
    from google.genai.types import Content, Part
    
    # Get any custom context from state
    custom_context = callback_context.state.get("custom_context")
    
    if custom_context and llm_request:
        # Add context as a system message at the beginning
        context_content = Content(parts=[
            Part(text=f"[System Context]: {custom_context}")
        ])
        return [context_content] + llm_request
    
    return None


def response_filter_callback(
    callback_context: CallbackContext,
    llm_response: Content,
) -> Optional[Content]:
    """
    Filter model responses for sensitive content.
    """
    from google.genai.types import Content, Part
    
    # List of sensitive patterns (in production, use a proper filter)
    sensitive_patterns = ["password:", "api_key:", "secret:"]
    
    if llm_response and llm_response.parts:
        for part in llm_response.parts:
            if hasattr(part, 'text') and part.text:
                for pattern in sensitive_patterns:
                    if pattern in part.text.lower():
                        # Replace sensitive content
                        filtered_text = part.text
                        for p in sensitive_patterns:
                            filtered_text = filtered_text.replace(p, "[REDACTED]:")
                        return Content(parts=[Part(text=filtered_text)])
    
    return None


"""
Model Callback Patterns
=======================

1. Request Logging
------------------
agent = LlmAgent(
    name="logged_agent",
    before_model_callback=model_logging_callback
)

2. Rate Limiting
----------------
agent = LlmAgent(
    name="rate_limited_agent",
    before_model_callback=rate_limit_callback
)

3. Context Injection
--------------------
agent = LlmAgent(
    name="context_agent",
    before_model_callback=context_injection_callback
)

4. Response Filtering
---------------------
agent = LlmAgent(
    name="filtered_agent",
    after_model_callback=response_filter_callback
)

5. Combined Callbacks
---------------------
agent = LlmAgent(
    name="full_callbacks_agent",
    before_model_callback=model_logging_callback,
    after_model_callback=response_filter_callback
)
"""
