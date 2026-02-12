"""
Built-in planner for Google ADK.

The BuiltInPlanner uses Gemini 2's native planning capability
to break down complex tasks into steps.
"""

from typing import Optional

from google.adk.planners import BuiltInPlanner


def create_builtin_planner(
    thinking_config: Optional[dict] = None,
) -> BuiltInPlanner:
    """
    Create a built-in planner using Gemini's native planning.
    
    The BuiltInPlanner leverages Gemini 2's "thinking" feature
    for planning. It creates internal plans before executing.
    
    Args:
        thinking_config: Optional configuration for thinking mode.
    
    Returns:
        BuiltInPlanner: A configured built-in planner.
    
    Example:
        planner = create_builtin_planner()
        agent = LlmAgent(
            name="planning_agent",
            planner=planner
        )
    
    Note:
        Requires a model that supports thinking (e.g., gemini-2.5-flash).
        The planner automatically creates step-by-step plans.
    """
    return BuiltInPlanner(
        thinking_config=thinking_config,
    )


# Pre-configured built-in planner
builtin_planner = BuiltInPlanner()


"""
Built-In Planner Usage
======================

The BuiltInPlanner enables Gemini's native planning capability.
When enabled, the model will:

1. Analyze the request
2. Create an internal plan
3. Execute steps one by one
4. Adapt the plan as needed

Example usage:
--------------

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner

agent = LlmAgent(
    name="planner_agent",
    model="gemini-2.5-flash",
    instruction="You solve complex tasks step by step.",
    planner=BuiltInPlanner(),
    tools=[...],
)

Benefits:
---------
- Handles complex multi-step tasks
- Adapts to new information
- Provides structured approach to problem-solving
- Works well with tool-heavy agents

Best used for:
--------------
- Research tasks with multiple sources
- Data analysis pipelines
- Complex API operations
- Multi-tool orchestration
"""
