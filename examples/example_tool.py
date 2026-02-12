"""
Example tool and provider for Google ADK.

The ExampleTool provides example outputs to guide agent behavior.
This is useful for few-shot learning and ensuring consistent outputs.
"""

from typing import Optional, List, Any, Dict
from abc import ABC, abstractmethod

from google.adk.tools import ExampleTool
from google.adk.examples import BaseExampleProvider, Example


class ExampleProvider(BaseExampleProvider):
    """
    Custom example provider implementation.
    
    Provides examples to ExampleTool based on various criteria.
    This can be extended to load examples from files, databases,
    or generate them dynamically.
    """
    
    def __init__(self, examples: Optional[List[Example]] = None):
        """
        Initialize the example provider.
        
        Args:
            examples: List of pre-defined examples.
        """
        self._examples = examples or []
    
    def get_examples(
        self,
        query: Optional[str] = None,
        limit: int = 3,
    ) -> List[Example]:
        """
        Get relevant examples for a query.
        
        Args:
            query: Optional query to filter examples.
            limit: Maximum number of examples to return.
        
        Returns:
            List[Example]: Relevant examples.
        """
        if not query:
            return self._examples[:limit]
        
        # Simple keyword matching
        query_lower = query.lower()
        relevant = [
            ex for ex in self._examples
            if query_lower in str(ex).lower()
        ]
        return relevant[:limit] or self._examples[:limit]
    
    def add_example(self, example: Example):
        """Add an example to the provider."""
        self._examples.append(example)


def create_example_tool(
    examples: Optional[List[Dict[str, Any]]] = None,
    provider: Optional[BaseExampleProvider] = None,
) -> ExampleTool:
    """
    Create an example tool.
    
    The ExampleTool provides few-shot examples to guide agent outputs.
    Examples show the expected format and content of responses.
    
    Args:
        examples: List of example dictionaries with input/output pairs.
        provider: Custom example provider for dynamic examples.
    
    Returns:
        ExampleTool: A configured example tool.
    
    Example:
        examples = [
            {
                "input": "What is 2+2?",
                "output": "The answer is 4."
            },
            {
                "input": "What is the capital of France?",
                "output": "The capital of France is Paris."
            }
        ]
        tool = create_example_tool(examples=examples)
    """
    return ExampleTool(
        examples=examples or [],
        provider=provider,
    )


# Pre-configured example tool with sample examples
example_tool = ExampleTool(
    examples=[
        {
            "input": "Search for Python tutorials",
            "output": "I'll search for Python tutorials using Google Search. Here are the top results: [list of tutorials with descriptions and URLs]"
        },
        {
            "input": "Calculate 15% of 250",
            "output": "15% of 250 is 37.5. Here's the calculation: 250 × 0.15 = 37.5"
        },
        {
            "input": "Create a calendar event for tomorrow at 2pm",
            "output": "I'll create a calendar event for tomorrow at 2:00 PM. Please provide a title for the event."
        },
    ],
)


"""
Example Tool Usage Patterns
===========================

1. Static Examples
------------------
Provide fixed examples for consistent behavior.

tool = ExampleTool(examples=[
    {"input": "...", "output": "..."},
    {"input": "...", "output": "..."},
])

2. Dynamic Provider
-------------------
Use a provider for context-aware examples.

class MyProvider(BaseExampleProvider):
    def get_examples(self, query):
        # Load from database, filter by query, etc.
        return relevant_examples

tool = ExampleTool(provider=MyProvider())

3. Combined Approach
--------------------
Use static examples with a provider fallback.

tool = ExampleTool(
    examples=static_examples,
    provider=dynamic_provider
)

Benefits:
---------
- Guides agent output format
- Provides few-shot learning context
- Ensures consistent response patterns
- Helps with domain-specific terminology

Use with LlmAgent:
------------------
agent = LlmAgent(
    name="example_guided_agent",
    instruction="Follow the examples for response format.",
    tools=[example_tool, other_tools...]
)
"""
