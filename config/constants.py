"""
Shared constants for the Google ADK Multi-Agent System.

This module contains all constant values used across the system including:
- Model names
- Agent names and descriptions
- Workflow configurations
- Default prompts
"""

# =============================================================================
# Model Constants
# =============================================================================

# Primary model for most agents
DEFAULT_MODEL = "gemini-2.5-flash"

# Model with extended thinking capabilities
THINKING_MODEL = "gemini-2.5-pro"

# Gemma model for specific use cases
GEMMA_MODEL = "gemma-3-27b-it"

# =============================================================================
# Agent Name Constants
# =============================================================================

# Core Orchestrator
ORCHESTRATOR_AGENT_NAME = "orchestrator"

# Specialized Agents
RESEARCH_AGENT_NAME = "research_agent"
CODE_AGENT_NAME = "code_execution_agent"
DATA_AGENT_NAME = "data_analysis_agent"
INTEGRATION_AGENT_NAME = "integration_agent"
MEMORY_AGENT_NAME = "memory_agent"

# Workflow Agent Names
SEQUENTIAL_PIPELINE_NAME = "sequential_pipeline"
PARALLEL_SEARCH_NAME = "parallel_search"
LOOP_REFINEMENT_NAME = "loop_refinement"

# Sub-agents for Sequential Pipeline
DATA_COLLECTOR_NAME = "data_collector"
DATA_PROCESSOR_NAME = "data_processor"
REPORT_GENERATOR_NAME = "report_generator"

# Sub-agents for Parallel Search
WEB_SEARCHER_NAME = "web_searcher"
DOC_SEARCHER_NAME = "doc_searcher"
CODE_SEARCHER_NAME = "code_searcher"

# Sub-agents for Loop Refinement
ANALYZER_NAME = "analyzer"
REFINER_NAME = "refiner"

# =============================================================================
# Agent Descriptions
# =============================================================================

AGENT_DESCRIPTIONS = {
    ORCHESTRATOR_AGENT_NAME: (
        "The main orchestrator agent that coordinates all other agents. "
        "It analyzes user requests and delegates tasks to the appropriate specialized agent."
    ),
    RESEARCH_AGENT_NAME: (
        "Specializes in web research, search operations, and information retrieval. "
        "Uses Google Search, URL context, and Vertex AI Search tools."
    ),
    CODE_AGENT_NAME: (
        "Handles code execution, analysis, and generation. "
        "Uses code executors to run Python code and analyze results."
    ),
    DATA_AGENT_NAME: (
        "Specializes in data analysis and BigQuery operations. "
        "Can query databases, analyze data, and generate insights."
    ),
    INTEGRATION_AGENT_NAME: (
        "Manages integrations with Google APIs including Calendar, Gmail, Docs, Sheets, and YouTube. "
        "Handles OAuth authentication and API operations."
    ),
    MEMORY_AGENT_NAME: (
        "Manages memory operations including loading, searching, and preloading memories. "
        "Also handles artifact management."
    ),
    SEQUENTIAL_PIPELINE_NAME: (
        "A sequential workflow that processes data through multiple stages in order."
    ),
    PARALLEL_SEARCH_NAME: (
        "A parallel workflow that performs multiple searches concurrently."
    ),
    LOOP_REFINEMENT_NAME: (
        "An iterative workflow that refines results through multiple passes."
    ),
}

# =============================================================================
# Instruction Templates (Variables for mixed approach)
# =============================================================================

ORCHESTRATOR_INSTRUCTION = """You are the main orchestrator for a multi-agent AI system.

Your role is to:
1. Understand user requests and determine which specialized agent should handle them
2. Transfer control to the appropriate agent using the transfer_to_agent tool
3. Coordinate complex tasks that may require multiple agents

Available agents you can transfer to:
- research_agent: For web searches, information retrieval, and research tasks
- code_execution_agent: For code execution, analysis, and generation
- data_analysis_agent: For BigQuery operations and data analysis
- integration_agent: For Google API integrations (Calendar, Gmail, Docs, etc.)
- memory_agent: For memory and artifact management
- sequential_pipeline: For multi-stage data processing workflows
- parallel_search: For concurrent search operations
- loop_refinement: For iterative refinement tasks

Always choose the most appropriate agent for the task. If unsure, ask the user for clarification.
"""

RESEARCH_INSTRUCTION = """You are a research specialist agent with access to powerful search and retrieval tools.

Your capabilities include:
- Web searching with Google Search
- Retrieving content from URLs
- Searching enterprise data with Vertex AI Search
- Maps-based grounding for location queries

When conducting research:
1. Use multiple sources when possible
2. Verify information across sources
3. Provide clear citations for your findings
4. Summarize key findings concisely

Always be thorough but efficient in your research approach.
"""

CODE_EXECUTION_INSTRUCTION = """You are a code execution specialist agent.

Your capabilities include:
- Executing Python code safely
- Analyzing code for bugs and improvements
- Generating code solutions
- Running data analysis scripts

Guidelines:
1. Always explain what code you're about to execute
2. Handle errors gracefully
3. Provide clear output explanations
4. Use safe coding practices

You can execute code to solve problems, analyze data, or demonstrate concepts.
"""

DATA_ANALYSIS_INSTRUCTION = """You are a data analysis specialist with BigQuery expertise.

Your capabilities include:
- Querying BigQuery datasets
- Performing data analysis
- Generating insights from data
- Creating data summaries

Guidelines:
1. Write efficient SQL queries
2. Explain your analysis approach
3. Visualize results when helpful
4. Provide actionable insights
"""

INTEGRATION_INSTRUCTION = """You are a Google API integration specialist.

Your capabilities include:
- Calendar: Create, read, update events
- Gmail: Read and send emails
- Docs: Create and edit documents
- Sheets: Read and write spreadsheets
- Slides: Create presentations
- YouTube: Search and retrieve video information

Guidelines:
1. Always confirm before making changes
2. Handle authentication properly
3. Respect rate limits
4. Provide clear feedback on operations
"""

MEMORY_INSTRUCTION = """You are a memory management specialist agent.

Your capabilities include:
- Loading artifacts from storage
- Searching memory for relevant information
- Preloading context for other agents
- Managing session state

Guidelines:
1. Efficiently retrieve relevant memories
2. Organize information clearly
3. Maintain context across interactions
4. Clean up unused resources
"""

# =============================================================================
# Workflow Instructions
# =============================================================================

SEQUENTIAL_PIPELINE_INSTRUCTION = """You are part of a sequential data processing pipeline.
Complete your specific task and pass the results to the next stage."""

PARALLEL_SEARCH_INSTRUCTION = """You are part of a parallel search operation.
Focus on your specific search domain and return comprehensive results."""

LOOP_REFINEMENT_INSTRUCTION = """You are part of an iterative refinement loop.
Analyze the current state and suggest improvements. Exit when quality is satisfactory."""

# =============================================================================
# Default Configuration Values
# =============================================================================

DEFAULT_MAX_LLM_CALLS = 500
DEFAULT_MAX_LOOP_ITERATIONS = 5
DEFAULT_SIMILARITY_TOP_K = 10
DEFAULT_VECTOR_DISTANCE_THRESHOLD = 10.0

# =============================================================================
# Tool Configuration Constants
# =============================================================================

# OpenAPI spec for demo REST API
SAMPLE_OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Sample API",
        "version": "1.0.0",
        "description": "A sample API for demonstration"
    },
    "servers": [
        {"url": "https://api.example.com/v1"}
    ],
    "paths": {
        "/items": {
            "get": {
                "operationId": "list_items",
                "summary": "List all items",
                "responses": {
                    "200": {
                        "description": "Successful response"
                    }
                }
            }
        },
        "/items/{id}": {
            "get": {
                "operationId": "get_item",
                "summary": "Get an item by ID",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response"
                    }
                }
            }
        }
    }
}
