"""
Parallel workflow agent - executes tasks concurrently.

The ParallelAgent executes all sub-agents simultaneously and
aggregates their outputs. Useful for multi-source searches or
independent parallel tasks.

Demonstrates:
- ParallelAgent for concurrent execution
- Multi-source search patterns
- Output aggregation
"""

from typing import Optional

from google.adk.agents import ParallelAgent, LlmAgent
from google.adk.tools import (
    GoogleSearchTool,
    UrlContextTool,
    FunctionTool,
)

from config.constants import (
    PARALLEL_SEARCH_NAME,
    WEB_SEARCHER_NAME,
    DOC_SEARCHER_NAME,
    CODE_SEARCHER_NAME,
    DEFAULT_MODEL,
    AGENT_DESCRIPTIONS,
)
from config.settings import get_settings
from tools.builtin_tools import (
    get_google_search_tool,
    get_url_context_tool,
    get_vertex_ai_search_tool,
)
from tools.custom_functions import fetch_url_content


def create_web_searcher_agent() -> LlmAgent:
    """Create the web search agent for parallel search."""
    return LlmAgent(
        name=WEB_SEARCHER_NAME,
        model="gemini-2.5-flash",  # Direct string
        description="Searches the web for general information",
        instruction="""You are a web search specialist in a parallel search team.

Your role is to search the web for relevant information on the given topic.
Focus on:
- Recent news and articles
- General knowledge sources
- Wikipedia and encyclopedic content

Output format:
- Key findings (3-5 bullet points)
- Source URLs
- Relevance score (high/medium/low)

Be thorough but focused. Your results will be combined with other searchers.
""",
        tools=[
            get_google_search_tool(bypass_multi_tools_limit=True),
            get_url_context_tool(),
        ],
    )


def create_doc_searcher_agent() -> LlmAgent:
    """Create the documentation search agent for parallel search."""
    settings = get_settings()
    
    return LlmAgent(
        name=DOC_SEARCHER_NAME,
        model=settings.models.default_model,  # From settings
        description="Searches documentation and technical resources",
        instruction="""You are a documentation specialist in a parallel search team.

Your role is to find technical documentation and guides on the given topic.
Focus on:
- Official documentation
- Technical specifications
- API references
- Tutorials and guides

Output format:
- Key findings (3-5 bullet points)
- Documentation links
- Relevance score (high/medium/low)

Prioritize official and authoritative sources.
""",
        tools=[
            get_google_search_tool(bypass_multi_tools_limit=True),
            FunctionTool(fetch_url_content),
        ],
    )


def create_code_searcher_agent() -> LlmAgent:
    """Create the code search agent for parallel search."""
    return LlmAgent(
        name=CODE_SEARCHER_NAME,
        model=DEFAULT_MODEL,  # From constant
        description="Searches for code examples and implementations",
        instruction="""You are a code search specialist in a parallel search team.

Your role is to find code examples and implementations for the given topic.
Focus on:
- GitHub repositories
- Code snippets and examples
- Stack Overflow solutions
- Open source implementations

Output format:
- Key code examples (with brief descriptions)
- Repository/source links
- Language/framework information
- Relevance score (high/medium/low)

Look for practical, working code examples.
""",
        tools=[
            get_google_search_tool(bypass_multi_tools_limit=True),
        ],
    )


def create_parallel_search() -> ParallelAgent:
    """
    Create a parallel multi-source search agent.
    
    The parallel search runs three specialized searchers concurrently:
    1. Web Searcher - General web content
    2. Doc Searcher - Technical documentation
    3. Code Searcher - Code examples and implementations
    
    Returns:
        ParallelAgent: A configured parallel search agent.
    
    Example:
        parallel = create_parallel_search()
        # Run: "Find information about Python async"
        # All three searchers run simultaneously
    """
    return ParallelAgent(
        name=PARALLEL_SEARCH_NAME,
        description=AGENT_DESCRIPTIONS.get(
            PARALLEL_SEARCH_NAME,
            "A parallel workflow that performs multiple searches concurrently."
        ),
        sub_agents=[
            create_web_searcher_agent(),
            create_doc_searcher_agent(),
            create_code_searcher_agent(),
        ],
    )


# Pre-configured parallel search instance
# Demonstrates compact inline definition
parallel_search = ParallelAgent(
    name=PARALLEL_SEARCH_NAME,
    description="Concurrent multi-source search: web + docs + code",
    sub_agents=[
        # Web Searcher
        LlmAgent(
            name=WEB_SEARCHER_NAME,
            model="gemini-2.5-flash",
            description="Searches web for general info",
            instruction="Search the web. Return 3-5 key findings with sources.",
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        ),
        # Documentation Searcher
        LlmAgent(
            name=DOC_SEARCHER_NAME,
            model="gemini-2.5-flash",
            description="Searches technical documentation",
            instruction="Find technical docs. Return 3-5 key findings with sources.",
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        ),
        # Code Searcher
        LlmAgent(
            name=CODE_SEARCHER_NAME,
            model="gemini-2.5-flash",
            description="Searches for code examples",
            instruction="Find code examples. Return 3-5 examples with sources.",
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        ),
    ],
)
