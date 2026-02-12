"""
Data analysis agent - specialized for BigQuery and data operations.

This agent demonstrates:
- BigQueryToolset for database operations
- Custom BigQuery toolset with hand-crafted tools
- Code executor for data processing
- Function tools for data manipulation
"""

from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.code_executors import BuiltInCodeExecutor

from config.constants import (
    DATA_AGENT_NAME,
    DATA_ANALYSIS_INSTRUCTION,
    AGENT_DESCRIPTIONS,
)
from config.settings import get_settings
from tools.google_api_tools import get_bigquery_toolset
from tools.custom_functions import calculate_expression, analyze_sentiment


# Data analysis instruction as variable
DATA_AGENT_INSTRUCTION = """You are a data analysis specialist with expertise in BigQuery and data processing.

Your capabilities:
- Query BigQuery datasets using SQL
- Analyze data patterns and trends
- Generate statistical insights
- Process and transform data
- Create data visualizations (with code executor)

Guidelines:
1. Write efficient, optimized SQL queries
2. Explain your analysis approach before executing
3. Provide clear interpretations of results
4. Suggest visualizations when appropriate
5. Handle large datasets with appropriate limits

BigQuery Best Practices:
- Use appropriate WHERE clauses to limit data
- Avoid SELECT * for large tables
- Use LIMIT for exploratory queries
- Explain query costs when relevant

Analysis Workflow:
1. Understand the data question
2. Explore available tables/columns
3. Write and execute queries
4. Analyze and interpret results
5. Present findings clearly
"""


def create_data_agent(
    model: Optional[str] = None,
    use_custom_bigquery: bool = False,
    include_code_executor: bool = True,
) -> LlmAgent:
    """
    Create the data analysis agent.
    
    The data agent specializes in BigQuery operations and data analysis
    with optional code execution for advanced processing.
    
    Args:
        model: Model to use. Defaults to settings.
        use_custom_bigquery: Use custom BigQuery toolset instead of auto-generated.
        include_code_executor: Include code executor for data processing.
    
    Returns:
        LlmAgent: The configured data analysis agent.
    
    Example:
        # Basic data agent
        data = create_data_agent()
        
        # With custom BigQuery tools
        data = create_data_agent(use_custom_bigquery=True)
    """
    settings = get_settings()
    
    # Build tools list
    tools = []
    
    # Add BigQuery toolset
    tools.append(get_bigquery_toolset(use_custom=use_custom_bigquery))
    
    # Add utility function tools
    tools.append(FunctionTool(calculate_expression))
    tools.append(FunctionTool(analyze_sentiment))
    
    # Code executor for data processing
    code_executor = None
    if include_code_executor:
        code_executor = BuiltInCodeExecutor(
            optimize_data_file_access=True,
        )
    
    return LlmAgent(
        name=DATA_AGENT_NAME,
        model=model or settings.models.default_model,
        description=AGENT_DESCRIPTIONS[DATA_AGENT_NAME],
        instruction=DATA_AGENT_INSTRUCTION,  # Using local variable
        tools=tools,
        code_executor=code_executor,
        disallow_transfer_to_parent=False,
    )


# Pre-configured data analysis agent
# Uses settings for model and BigQuery configuration
settings = get_settings()

data_analysis_agent = LlmAgent(
    name=DATA_AGENT_NAME,
    model=settings.models.default_model,  # From settings
    description=AGENT_DESCRIPTIONS[DATA_AGENT_NAME],  # From constants
    instruction=DATA_ANALYSIS_INSTRUCTION,  # From constants
    tools=[
        get_bigquery_toolset(),  # From factory function
        FunctionTool(calculate_expression),
        FunctionTool(analyze_sentiment),
    ],
    code_executor=BuiltInCodeExecutor(
        optimize_data_file_access=True,
    ),
)
