"""
Code execution agent - specialized for running and analyzing code.

This agent demonstrates:
- BuiltInCodeExecutor: Safe code execution in sandbox
- UnsafeLocalCodeExecutor: Local code execution (use with caution)
- CodeExecutorContext: Context management for code execution
- Function tools for code analysis
"""

from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.code_executors import (
    BuiltInCodeExecutor,
    UnsafeLocalCodeExecutor,
    CodeExecutorContext,
)
from google.adk.tools import FunctionTool

from config.constants import (
    CODE_AGENT_NAME,
    CODE_EXECUTION_INSTRUCTION,
    AGENT_DESCRIPTIONS,
    DEFAULT_MODEL,
)
from config.settings import get_settings
from tools.custom_functions import calculate_expression


def create_code_agent(
    model: Optional[str] = None,
    use_unsafe_executor: bool = False,
    optimize_data_file_access: bool = False,
    stateful_execution: bool = True,
) -> LlmAgent:
    """
    Create the code execution agent.
    
    The code agent can execute Python code using either the built-in
    sandbox executor or the unsafe local executor.
    
    Args:
        model: Model to use. Defaults to settings.
        use_unsafe_executor: If True, use UnsafeLocalCodeExecutor.
                            Use with caution - runs on local machine!
        optimize_data_file_access: Optimize for data file operations.
        stateful_execution: Maintain state across code executions.
    
    Returns:
        LlmAgent: The configured code execution agent.
    
    Warning:
        UnsafeLocalCodeExecutor runs code on your local machine without
        sandboxing. Only use in trusted environments with trusted input.
    
    Example:
        # Safe built-in executor
        code_agent = create_code_agent()
        
        # Unsafe local executor (be careful!)
        code_agent = create_code_agent(use_unsafe_executor=True)
    """
    settings = get_settings()
    
    # Choose code executor
    if use_unsafe_executor:
        # UnsafeLocalCodeExecutor - runs on local machine
        # WARNING: This executes arbitrary code without sandboxing!
        code_executor = UnsafeLocalCodeExecutor(
            stateful=stateful_execution,
        )
    else:
        # BuiltInCodeExecutor - uses Gemini's built-in code execution
        code_executor = BuiltInCodeExecutor(
            optimize_data_file_access=optimize_data_file_access,
        )
    
    # Additional tools for code-related tasks
    tools = [
        FunctionTool(calculate_expression),  # Math calculations
    ]
    
    return LlmAgent(
        name=CODE_AGENT_NAME,
        model=model or settings.models.default_model,
        description=AGENT_DESCRIPTIONS[CODE_AGENT_NAME],
        instruction=CODE_EXECUTION_INSTRUCTION,
        tools=tools,
        code_executor=code_executor,  # Attach code executor
        disallow_transfer_to_parent=False,
    )


def create_code_agent_with_context() -> tuple[LlmAgent, CodeExecutorContext]:
    """
    Create code agent with an explicit CodeExecutorContext.
    
    The CodeExecutorContext allows inspection and modification of
    the code execution environment.
    
    Returns:
        tuple: (LlmAgent, CodeExecutorContext)
    
    Example:
        agent, context = create_code_agent_with_context()
        # Inspect context after execution
        print(context.global_vars)
    """
    context = CodeExecutorContext()
    
    executor = UnsafeLocalCodeExecutor(
        stateful=True,
    )
    
    agent = LlmAgent(
        name=CODE_AGENT_NAME,
        model=DEFAULT_MODEL,
        description="Code execution with context inspection",
        instruction=CODE_EXECUTION_INSTRUCTION,
        code_executor=executor,
    )
    
    return agent, context


# Pre-configured code execution agent
# Using BuiltInCodeExecutor (safe sandbox)
code_execution_agent = LlmAgent(
    name=CODE_AGENT_NAME,
    model="gemini-2.5-flash",  # Direct string
    description="Handles code execution, analysis, and generation with safe sandbox.",
    instruction="""You are a code execution specialist with access to a Python sandbox.

Your capabilities:
- Execute Python code safely in a sandbox environment
- Analyze code for bugs, improvements, and optimizations
- Generate code solutions for various problems
- Run data analysis scripts and visualizations

Guidelines for code execution:
1. Always explain what the code will do before running it
2. Handle errors gracefully and provide helpful error messages
3. Use appropriate libraries for the task (pandas, numpy, matplotlib, etc.)
4. Provide clear explanations of the output
5. Suggest improvements when appropriate

Safety:
- The code runs in a sandboxed environment
- External network access may be limited
- File system access is restricted
- Be mindful of execution time

When writing code:
- Use clear variable names
- Add comments for complex logic
- Break down large tasks into smaller functions
- Validate inputs where appropriate
""",  # Direct instruction
    tools=[
        FunctionTool(calculate_expression),
    ],
    code_executor=BuiltInCodeExecutor(
        optimize_data_file_access=True,
    ),  # Direct executor instantiation
)
