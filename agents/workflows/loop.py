"""
Loop workflow agent - iterates until condition is met.

The LoopAgent repeatedly executes sub-agents until a termination
condition is met. Useful for iterative refinement tasks.

Demonstrates:
- LoopAgent for iterative execution
- Termination conditions
- Refinement patterns
"""

from typing import Optional, Callable

from google.adk.agents import LoopAgent, LlmAgent, Agent
from google.adk.tools import FunctionTool

from config.constants import (
    LOOP_REFINEMENT_NAME,
    ANALYZER_NAME,
    REFINER_NAME,
    DEFAULT_MODEL,
    AGENT_DESCRIPTIONS,
    DEFAULT_MAX_LOOP_ITERATIONS,
)
from config.settings import get_settings
from tools.custom_functions import analyze_sentiment, format_text


def create_analyzer_agent() -> LlmAgent:
    """Create the analysis agent for the refinement loop."""
    return LlmAgent(
        name=ANALYZER_NAME,
        model="gemini-2.5-flash",  # Direct string
        description="Analyzes content quality and identifies issues",
        instruction="""You are an analysis agent in an iterative refinement loop.

Your role is to evaluate the current content and identify areas for improvement.

Analysis criteria:
1. Clarity - Is the content clear and understandable?
2. Completeness - Are all key points covered?
3. Accuracy - Is the information accurate?
4. Structure - Is it well-organized?
5. Style - Is the tone appropriate?

Output format:
- Overall quality score (1-10)
- Specific issues found
- Recommended improvements
- DONE if quality >= 8 and no major issues

Include 'DONE' in your response when the content meets quality standards.
""",
        tools=[
            FunctionTool(analyze_sentiment),
        ],
    )


def create_refiner_agent() -> LlmAgent:
    """Create the refinement agent for the loop."""
    settings = get_settings()
    
    refiner_instruction = """You are a refinement agent in an iterative improvement loop.

You receive analysis feedback and must improve the content accordingly.

Refinement process:
1. Review the analysis feedback
2. Address each identified issue
3. Improve overall quality
4. Maintain the original intent

Output the improved content directly.
Focus on the most impactful improvements first.
"""
    
    return LlmAgent(
        name=REFINER_NAME,
        model=settings.models.default_model,  # From settings
        description="Refines content based on analysis feedback",
        instruction=refiner_instruction,  # Local variable
        tools=[
            FunctionTool(format_text),
        ],
    )


def quality_check_termination(response: str) -> bool:
    """
    Termination condition based on quality check.
    
    Returns True to stop the loop when:
    - "DONE" appears in the response
    - Quality score >= 8 is mentioned
    
    Args:
        response: The agent's response to check.
    
    Returns:
        bool: True if loop should terminate.
    """
    response_lower = response.lower()
    
    # Check for explicit DONE signal
    if "done" in response_lower:
        return True
    
    # Check for high quality score
    import re
    score_match = re.search(r'quality[:\s]+(\d+)', response_lower)
    if score_match:
        score = int(score_match.group(1))
        if score >= 8:
            return True
    
    return False


def create_loop_refinement(
    max_iterations: int = DEFAULT_MAX_LOOP_ITERATIONS,
) -> LoopAgent:
    """
    Create an iterative refinement loop agent.
    
    The loop consists of two stages that repeat until quality is satisfactory:
    1. Analyzer - Evaluates content and identifies issues
    2. Refiner - Improves content based on feedback
    
    Args:
        max_iterations: Maximum number of loop iterations.
    
    Returns:
        LoopAgent: A configured loop refinement agent.
    
    Example:
        loop = create_loop_refinement(max_iterations=3)
        # Run: "Improve this draft: [content]"
        # Loop: analyze -> refine -> analyze -> ... until DONE
    """
    return LoopAgent(
        name=LOOP_REFINEMENT_NAME,
        description=AGENT_DESCRIPTIONS.get(
            LOOP_REFINEMENT_NAME,
            "An iterative workflow that refines results through multiple passes."
        ),
        sub_agents=[
            create_analyzer_agent(),
            create_refiner_agent(),
        ],
        max_iterations=max_iterations,
    )


# Pre-configured loop refinement instance
# Using inline sub-agents
loop_refinement = LoopAgent(
    name=LOOP_REFINEMENT_NAME,
    description="Iterative content refinement: analyze → refine → repeat until quality met",
    sub_agents=[
        # Analyzer
        LlmAgent(
            name=ANALYZER_NAME,
            model="gemini-2.5-flash",
            description="Analyzes content quality",
            instruction="""Analyze the content for quality.
Score from 1-10 on: clarity, completeness, accuracy, structure.
List specific issues. Say 'DONE' if score >= 8.""",
            tools=[FunctionTool(analyze_sentiment)],
        ),
        # Refiner
        LlmAgent(
            name=REFINER_NAME,
            model="gemini-2.5-flash",
            description="Refines content based on feedback",
            instruction="Improve the content based on the analysis feedback. Output refined version.",
            tools=[FunctionTool(format_text)],
        ),
    ],
    max_iterations=DEFAULT_MAX_LOOP_ITERATIONS,  # From constant
)


# Alternative: SequentialAgent inside LoopAgent for more control
def create_sequential_refinement_loop() -> LoopAgent:
    """
    Create a loop with a sequential inner workflow.
    
    This demonstrates nesting workflow agents - a LoopAgent
    containing a SequentialAgent.
    
    Returns:
        LoopAgent: A loop with sequential inner stages.
    """
    from google.adk.agents import SequentialAgent
    
    # Inner sequential workflow
    inner_sequence = SequentialAgent(
        name="refinement_sequence",
        description="Sequential refinement stages",
        sub_agents=[
            create_analyzer_agent(),
            create_refiner_agent(),
        ],
    )
    
    # Outer loop
    return LoopAgent(
        name="sequential_loop_refinement",
        description="Loop containing sequential refinement",
        sub_agents=[inner_sequence],
        max_iterations=3,
    )
