"""
Plan-ReAct planner for Google ADK.

The PlanReActPlanner implements the Plan-and-ReAct pattern,
which creates an explicit plan and then executes it with
reasoning and acting phases.
"""

from typing import Optional

from google.adk.planners import PlanReActPlanner


def create_plan_react_planner(
    max_planning_steps: int = 10,
    max_react_steps: int = 5,
) -> PlanReActPlanner:
    """
    Create a Plan-ReAct planner.
    
    The PlanReActPlanner creates an explicit multi-step plan
    before execution, then uses the ReAct (Reasoning + Acting)
    pattern to execute each step.
    
    Args:
        max_planning_steps: Maximum steps in the plan.
        max_react_steps: Maximum ReAct iterations per step.
    
    Returns:
        PlanReActPlanner: A configured Plan-ReAct planner.
    
    Example:
        planner = create_plan_react_planner(
            max_planning_steps=5,
            max_react_steps=3
        )
        agent = LlmAgent(
            name="react_agent",
            planner=planner
        )
    
    Plan-ReAct Pattern:
        1. PLAN: Break down task into steps
        2. For each step:
           - THINK: Reason about what to do
           - ACT: Execute tool or action
           - OBSERVE: Process the result
        3. Repeat until complete
    """
    return PlanReActPlanner(
        max_planning_steps=max_planning_steps,
        max_react_steps=max_react_steps,
    )


# Pre-configured Plan-ReAct planner
plan_react_planner = PlanReActPlanner(
    max_planning_steps=10,  # Direct value
    max_react_steps=5,       # Direct value
)


"""
Plan-ReAct Planner Usage
========================

The PlanReActPlanner implements a structured approach:

Phase 1: Planning
-----------------
The model creates an explicit multi-step plan:
- Step 1: Research the topic using search
- Step 2: Analyze the key findings
- Step 3: Generate a summary
- Step 4: Review and refine

Phase 2: Execution (ReAct)
--------------------------
For each planned step:
1. THINK: "I need to search for information about X"
2. ACT: Call search tool with query
3. OBSERVE: "Found 5 relevant results about X"
4. Repeat if needed for the step

Example:
--------

from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner

agent = LlmAgent(
    name="react_agent",
    model="gemini-2.5-flash",
    instruction="You methodically plan and execute tasks.",
    planner=PlanReActPlanner(
        max_planning_steps=10,
        max_react_steps=5,
    ),
    tools=[...],
)

Comparison with BuiltInPlanner:
-------------------------------
- BuiltInPlanner: Implicit planning in model's thinking
- PlanReActPlanner: Explicit, visible planning with structured execution

Use PlanReActPlanner when:
--------------------------
- You want visible, auditable plans
- Tasks have clear step-by-step structure
- Debugging execution flow is important
- You need to constrain planning depth
"""
