"""
Sequential workflow agent - processes tasks in order.

The SequentialAgent executes sub-agents in sequence, passing output
from one stage to the next. Useful for pipeline-style workflows.

Demonstrates:
- SequentialAgent for ordered execution
- Multi-stage data pipelines
- State passing between stages
"""

from typing import Optional, List

from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.tools import FunctionTool

from config.constants import (
    SEQUENTIAL_PIPELINE_NAME,
    DATA_COLLECTOR_NAME,
    DATA_PROCESSOR_NAME,
    REPORT_GENERATOR_NAME,
    DEFAULT_MODEL,
    AGENT_DESCRIPTIONS,
)
from config.settings import get_settings
from tools.builtin_tools import get_google_search_tool
from tools.custom_functions import format_text, analyze_sentiment


def create_data_collector_agent() -> LlmAgent:
    """Create the data collection stage agent."""
    return LlmAgent(
        name=DATA_COLLECTOR_NAME,
        model="gemini-2.5-flash",  # Direct string
        description="Collects raw data from various sources",
        instruction="""You are the data collection stage of a processing pipeline.

Your task is to gather raw data based on the given query or topic.
Use search tools to find relevant information and compile it.

Output format:
- List the sources you used
- Provide raw collected data
- Note any gaps or missing information

Your output will be passed to the next processing stage.
""",  # Direct instruction
        tools=[
            get_google_search_tool(bypass_multi_tools_limit=True),
        ],
    )


def create_data_processor_agent() -> LlmAgent:
    """Create the data processing stage agent."""
    return LlmAgent(
        name=DATA_PROCESSOR_NAME,
        model=DEFAULT_MODEL,  # Using constant
        description="Processes and analyzes collected data",
        instruction="""You are the data processing stage of a pipeline.

You receive raw data from the collection stage and must:
1. Clean and normalize the data
2. Extract key insights
3. Identify patterns and trends
4. Flag any inconsistencies

Output format:
- Summary of processed data
- Key findings and insights
- Data quality notes

Your output will be passed to the report generation stage.
""",  # Direct instruction
        tools=[
            FunctionTool(format_text),
            FunctionTool(analyze_sentiment),
        ],
    )


def create_report_generator_agent() -> LlmAgent:
    """Create the report generation stage agent."""
    settings = get_settings()
    
    report_instruction = """You are the final report generation stage of a pipeline.

You receive processed data and insights, and must generate a comprehensive report.

Report structure:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Recommendations
5. Data Sources

Make the report clear, professional, and actionable.
"""
    
    return LlmAgent(
        name=REPORT_GENERATOR_NAME,
        model=settings.models.default_model,  # Using settings
        description="Generates final reports from processed data",
        instruction=report_instruction,  # Local variable
        tools=[
            FunctionTool(format_text),
        ],
    )


def create_sequential_pipeline() -> SequentialAgent:
    """
    Create a sequential data processing pipeline.
    
    The pipeline consists of three stages:
    1. Data Collection - Gathers raw data
    2. Data Processing - Analyzes and transforms data
    3. Report Generation - Creates final output
    
    Returns:
        SequentialAgent: A configured sequential pipeline.
    
    Example:
        pipeline = create_sequential_pipeline()
        # Run: "Create a report on AI trends"
        # Pipeline: collect -> process -> report
    """
    return SequentialAgent(
        name=SEQUENTIAL_PIPELINE_NAME,
        description=AGENT_DESCRIPTIONS.get(
            SEQUENTIAL_PIPELINE_NAME,
            "A sequential workflow that processes data through multiple stages in order."
        ),
        sub_agents=[
            create_data_collector_agent(),
            create_data_processor_agent(),
            create_report_generator_agent(),
        ],
    )


# Pre-configured sequential pipeline instance
# Demonstrates inline sub-agent definition
sequential_pipeline = SequentialAgent(
    name=SEQUENTIAL_PIPELINE_NAME,
    description="Multi-stage data processing pipeline: collect → process → report",
    sub_agents=[
        # Stage 1: Data Collection
        LlmAgent(
            name=DATA_COLLECTOR_NAME,
            model="gemini-2.5-flash",
            description="Collects data from search",
            instruction="Collect relevant data using search tools. Output raw findings.",
            tools=[get_google_search_tool()],
        ),
        # Stage 2: Data Processing
        LlmAgent(
            name=DATA_PROCESSOR_NAME,
            model="gemini-2.5-flash",
            description="Processes collected data",
            instruction="Process the collected data. Extract insights and clean the data.",
            tools=[FunctionTool(analyze_sentiment)],
        ),
        # Stage 3: Report Generation
        LlmAgent(
            name=REPORT_GENERATOR_NAME,
            model="gemini-2.5-flash",
            description="Generates final report",
            instruction="Generate a comprehensive report from the processed data.",
            tools=[FunctionTool(format_text)],
        ),
    ],
)
