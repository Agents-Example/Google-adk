# Google ADK Multi-Agent Orchestration System

A comprehensive multi-agent system demonstrating **all** Google Agent Development Kit (ADK) capabilities, including all agent types, 50+ tools/toolsets, MCP integrations, code executors, planners, plugins, backend services, and observability platforms.

## Overview

This project serves as a complete reference implementation of Google ADK, showcasing:

- **All Agent Types**: `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`
- **50+ Tools/Toolsets**: Built-in tools, function tools, Google API toolsets, MCP tools, OpenAPI tools, enterprise tools
- **All MCP Connection Types**: `StdioConnectionParams`, `SseConnectionParams`, `StreamableHTTPConnectionParams`
- **14 MCP Server Integrations**: GitHub, Hugging Face, Notion, Stripe, ElevenLabs, PayPal, Linear, Atlassian, Asana, GitLab, Postman, N8N, Daytona, MCP Toolbox
- **8 Observability Platforms**: AgentOps, Arize AX, Phoenix, MLflow, Monocle, Cloud Trace, W&B Weave, Freeplay
- **Code Executors**: `BuiltInCodeExecutor`, `UnsafeLocalCodeExecutor`, `ComputerUseToolset`
- **Planners**: `BuiltInPlanner`, `PlanReActPlanner`
- **Plugins**: `LoggingPlugin`, `DebugLoggingPlugin`, `ReflectAndRetryToolPlugin`
- **All Backend Services**: InMemory and Vertex AI implementations for sessions, artifacts, and memory
- **Callbacks**: Agent, tool, and model callbacks for customization

## MCP Dataset

This project includes a comprehensive **MCP Dataset** (`mcp_dataset.json`) that documents all available tools and capabilities for AI SPM scanners:

```json
{
  "mcp_servers": [...],           // 14 MCP server integrations
  "google_cloud_integrations": [...], // Google Cloud specific tools
  "observability_platforms": [...],   // 8 observability integrations
  "builtin_tools": [...],         // Built-in Gemini tools
  "google_api_toolsets": [...],   // Google API toolsets
  "code_executors": [...],        // Code execution options
  "services": {...},              // Session, artifact, memory services
  "plugins": [...],               // Available plugins
  "planners": [...],              // Planner options
  "agent_types": [...]            // Agent type reference
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                            App / Runner                          │
├─────────────────────────────────────────────────────────────────┤
│                       Root Orchestrator                          │
│                         (LlmAgent)                               │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ Research │   Code   │   Data   │Integration│     Memory         │
│  Agent   │  Agent   │  Agent   │  Agent   │     Agent          │
├──────────┴──────────┴──────────┴──────────┴────────────────────┤
│            Workflow Agents (Sequential, Parallel, Loop)          │
├─────────────────────────────────────────────────────────────────┤
│               Backend Services (Session, Artifact, Memory)       │
├─────────────────────────────────────────────────────────────────┤
│                        Plugin System                             │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
google-adk/
├── config/                     # Configuration
│   ├── __init__.py
│   ├── settings.py            # Environment-based settings
│   └── constants.py           # Shared constants
├── services/                   # Backend services
│   ├── __init__.py
│   ├── session.py             # Session service factories
│   ├── artifact.py            # Artifact service factories
│   ├── memory.py              # Memory service factories
│   └── credential.py          # Credential management
├── tools/                      # Tool definitions
│   ├── __init__.py
│   ├── builtin_tools.py       # GoogleSearch, UrlContext, VertexAiSearch
│   ├── function_tools.py      # FunctionTool, LongRunningFunctionTool
│   ├── custom_functions.py    # Python functions for FunctionTool
│   ├── google_api_tools.py    # Calendar, Gmail, Docs, Sheets, etc.
│   ├── mcp_tools.py           # MCP toolsets (Stdio, SSE, HTTP)
│   ├── openapi_tools.py       # OpenAPIToolset, RestApiTool
│   ├── enterprise_tools.py    # APIHub, ApplicationIntegration, Toolbox
│   └── memory_tools.py        # LoadMemory, PreloadMemory, LoadArtifacts
├── integrations/               # Third-party integrations
│   ├── __init__.py
│   ├── observability.py       # AgentOps, Arize, Phoenix, MLflow, etc.
│   ├── mcp_integrations.py    # GitHub, Notion, Stripe, ElevenLabs, etc.
│   ├── database_integrations.py  # MCP Toolbox, Qdrant, Chroma
│   ├── google_cloud.py        # Express Mode, RAG, PubSub
│   ├── code_executors.py      # Computer Use, GKE Executor
│   └── ui_integrations.py     # AG-UI
├── agents/                     # Agent definitions
│   ├── __init__.py
│   ├── orchestrator/          # Root orchestrator agent
│   ├── research/              # Research agent
│   ├── code_execution/        # Code execution agent
│   ├── data_analysis/         # Data analysis agent
│   ├── integration/           # Google API integration agent
│   ├── memory/                # Memory management agent
│   ├── comprehensive/         # Uses ALL plugins/services/integrations
│   ├── mcp_hub/               # Uses ALL MCP integrations
│   ├── observability/         # Uses ALL observability platforms
│   └── workflows/             # Workflow agents
│       ├── __init__.py
│       ├── sequential.py      # SequentialAgent
│       ├── parallel.py        # ParallelAgent
│       └── loop.py            # LoopAgent
├── plugins/                    # Plugin implementations
│   ├── __init__.py
│   ├── logging.py             # LoggingPlugin, DebugLoggingPlugin
│   └── retry.py               # ReflectAndRetryToolPlugin
├── planners/                   # Planner configurations
│   ├── __init__.py
│   ├── builtin.py             # BuiltInPlanner
│   └── plan_react.py          # PlanReActPlanner
├── examples/                   # Example tools
│   ├── __init__.py
│   └── example_tool.py        # ExampleTool, BaseExampleProvider
├── callbacks/                  # Callback implementations
│   ├── __init__.py
│   ├── agent_callbacks.py     # Before/after agent callbacks
│   ├── tool_callbacks.py      # Before/after tool callbacks
│   └── model_callbacks.py     # Before/after model callbacks
├── mcp_dataset.json            # MCP capabilities dataset for AI SPM
├── app.py                      # App configuration (web UI)
├── runner.py                   # Runner configuration (programmatic)
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
├── .env.example                # Environment variables template
└── .gitignore
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 3. Run the System

**Web UI Mode:**
```bash
python main.py --mode web --port 8080
```

**Interactive CLI:**
```bash
python main.py --mode interactive
```

**Single Message:**
```bash
python main.py --mode cli --message "Search for Python tutorials"
```

**Demo Mode:**
```bash
python main.py --mode demo --demo full
```

## Tools Reference

### Built-in Gemini Tools

| Tool | Description |
|------|-------------|
| `GoogleSearchTool` | Web search grounding |
| `UrlContextTool` | URL content retrieval |
| `VertexAiSearchTool` | Vertex AI Search integration |
| `GoogleMapsGroundingTool` | Maps-based grounding (Vertex AI only) |
| `EnterpriseWebSearchTool` | Enterprise web search |
| `DiscoveryEngineSearchTool` | Discovery Engine search |

### Function Tools

| Tool | Description |
|------|-------------|
| `FunctionTool` | Wrap Python functions |
| `LongRunningFunctionTool` | Async long-running operations |
| `AuthenticatedFunctionTool` | Functions with authentication |

### Google API Toolsets

| Toolset | Description |
|---------|-------------|
| `CalendarToolset` | Google Calendar operations |
| `GmailToolset` | Gmail operations |
| `DocsToolset` | Google Docs operations |
| `SheetsToolset` | Google Sheets operations |
| `SlidesToolset` | Google Slides operations |
| `YoutubeToolset` | YouTube operations |
| `BigQueryToolset` | BigQuery operations |

### MCP Tools

| Tool/Connection | Description |
|-----------------|-------------|
| `McpToolset` | MCP server toolset |
| `StdioConnectionParams` | Local MCP servers (npx, python) |
| `SseConnectionParams` | SSE-based MCP servers |
| `StreamableHTTPConnectionParams` | HTTP-based MCP servers |
| `ApiRegistry` | API Registry integration |
| `McpInstructionProvider` | Dynamic instructions from MCP |

### Enterprise Tools

| Tool | Description |
|------|-------------|
| `APIHubToolset` | API Hub integration |
| `ApplicationIntegrationToolset` | Application Integration |
| `ToolboxToolset` | MCP Toolbox SDK |
| `OpenAPIToolset` | OpenAPI spec tools |
| `RestApiTool` | Individual REST API tools |

### Memory Tools

| Tool | Description |
|------|-------------|
| `LoadArtifactsTool` | Load saved artifacts |
| `LoadMemoryTool` | Search memories explicitly |
| `PreloadMemoryTool` | Auto-inject memory context |

### Agent Tools

| Tool | Description |
|------|-------------|
| `AgentTool` | Invoke another agent |
| `TransferToAgentTool` | Transfer control to agent |

## MCP Integrations

This project includes comprehensive MCP (Model Context Protocol) integrations:

### Code & DevOps

| MCP Server | Description | Env Var |
|------------|-------------|---------|
| GitHub | Repository, issues, PRs, actions | `GITHUB_TOKEN` |
| GitLab | Code management, CI/CD | `GITLAB_TOKEN` |
| Daytona | Development environments | `DAYTONA_API_KEY` |

### AI & ML

| MCP Server | Description | Env Var |
|------------|-------------|---------|
| Hugging Face | Models, datasets, papers | `HF_TOKEN` |
| ElevenLabs | TTS, voice cloning, audio | `ELEVENLABS_API_KEY` |

### Productivity

| MCP Server | Description | Env Var |
|------------|-------------|---------|
| Notion | Workspace, pages, databases | `NOTION_TOKEN` |
| Linear | Issue tracking | `LINEAR_API_KEY` |
| Atlassian | Jira, Confluence | `ATLASSIAN_API_TOKEN` |
| Asana | Task management | `ASANA_ACCESS_TOKEN` |

### Business & Payments

| MCP Server | Description | Env Var |
|------------|-------------|---------|
| Stripe | Payments, subscriptions | `STRIPE_SECRET_KEY` |
| PayPal | Payment processing | `PAYPAL_CLIENT_ID` |

### API & Automation

| MCP Server | Description | Env Var |
|------------|-------------|---------|
| Postman | API testing | `POSTMAN_API_KEY` |
| N8N | Workflow automation | `N8N_API_KEY` |

### Databases

| Integration | Description | Env Var |
|-------------|-------------|---------|
| MCP Toolbox | 30+ databases (BigQuery, PostgreSQL, MongoDB, Neo4j, etc.) | `TOOLBOX_SERVER_URL` |

## Observability Platforms

All 8 observability platforms documented in Google ADK are supported:

| Platform | Description | Setup |
|----------|-------------|-------|
| AgentOps | Session replays, metrics | `agentops.init()` |
| Arize AX | Production-grade observability | `GoogleADKInstrumentor().instrument()` |
| Phoenix | Open-source, self-hosted | `phoenix.otel.register()` |
| MLflow | OpenTelemetry ingestion | `OTLPSpanExporter` |
| Monocle | Open-source tracing | `setup_monocle_telemetry()` |
| Cloud Trace | Google Cloud native | `CloudTraceSpanExporter` |
| W&B Weave | Model call logging | `OTLPSpanExporter` |
| Freeplay | Testing and evaluation | API-based |

```python
from integrations.observability import (
    setup_agentops,
    setup_phoenix,
    setup_monocle,
)

# Enable multiple observability platforms
setup_agentops(trace_name="my-agent")
setup_phoenix(project_name="my-project")
setup_monocle(workflow_name="my-workflow")
```

## Special Agents

Three specialized agents demonstrate comprehensive usage of all capabilities:

### Comprehensive Agent
Uses ALL plugins, services, and integrations in one agent:

```python
from agents.comprehensive import comprehensive_agent

# This agent has:
# - All plugins (Logging, Debug, Retry)
# - All callbacks (before/after agent, tool, model)
# - All observability (AgentOps, Cloud Trace)
# - All MCP integrations (when env vars set)
# - All built-in and function tools
```

### MCP Hub Agent
Demonstrates ALL MCP server integrations:

```python
from agents.mcp_hub import mcp_hub_agent

# Access to: GitHub, Hugging Face, Notion, Stripe,
# ElevenLabs, PayPal, Linear, Atlassian, Asana,
# GitLab, Postman, N8N, Daytona, MCP Toolbox
```

### Observability Agent
Demonstrates ALL observability platforms:

```python
from agents.observability import observability_agent

# Traced by: AgentOps, Arize AX, Phoenix, MLflow,
# Monocle, Cloud Trace, W&B Weave, Freeplay
```

## Agent Types

### LlmAgent
The primary agent type with LLM capabilities, tools, and sub-agents.

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant.",
    tools=[...],
    sub_agents=[...],
    planner=BuiltInPlanner(),
    plugins=[LoggingPlugin()],
)
```

### SequentialAgent
Executes sub-agents in sequence.

```python
from google.adk.agents import SequentialAgent

pipeline = SequentialAgent(
    name="pipeline",
    sub_agents=[stage1, stage2, stage3],
)
```

### ParallelAgent
Executes sub-agents concurrently.

```python
from google.adk.agents import ParallelAgent

parallel = ParallelAgent(
    name="multi_search",
    sub_agents=[searcher1, searcher2, searcher3],
)
```

### LoopAgent
Executes sub-agents repeatedly until condition met.

```python
from google.adk.agents import LoopAgent

loop = LoopAgent(
    name="refinement",
    sub_agents=[analyzer, refiner],
    max_iterations=5,
)
```

## Backend Services

### Session Services

```python
# InMemory (development)
from services.session import create_inmemory_session_service
session_service = create_inmemory_session_service()

# Vertex AI (production)
from services.session import create_vertex_session_service
session_service = create_vertex_session_service(
    project="my-project",
    location="us-central1"
)
```

### Artifact Services

```python
# InMemory
from services.artifact import create_inmemory_artifact_service

# File-based
from services.artifact import create_file_artifact_service

# GCS (production)
from services.artifact import create_gcs_artifact_service
```

### Memory Services

```python
# InMemory
from services.memory import create_inmemory_memory_service

# Vertex AI Memory Bank
from services.memory import create_vertex_memory_bank_service

# Vertex AI RAG
from services.memory import create_vertex_rag_memory_service
```

## Callbacks

### Agent Callbacks

```python
def before_agent(ctx):
    print(f"Starting agent: {ctx.agent.name}")
    return None  # Continue execution

def after_agent(ctx):
    print(f"Finished agent: {ctx.agent.name}")
    return None  # Use original response

agent = LlmAgent(
    name="my_agent",
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
)
```

### Tool Callbacks

```python
def before_tool(ctx, name, args):
    print(f"Calling tool: {name}")
    return None  # Use original args

def after_tool(ctx, name, args, response):
    print(f"Tool returned: {type(response)}")
    return None  # Use original response

agent = LlmAgent(
    name="my_agent",
    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
)
```

## Configuration Patterns

This project demonstrates two patterns for providing configuration:

### 1. Variable-Based (Reusable)

```python
from config.constants import DEFAULT_MODEL, RESEARCH_INSTRUCTION

agent = LlmAgent(
    name="research",
    model=DEFAULT_MODEL,
    instruction=RESEARCH_INSTRUCTION,
)
```

### 2. Direct Inline (Simple)

```python
agent = LlmAgent(
    name="research",
    model="gemini-2.5-flash",
    instruction="You are a research assistant...",
)
```

## Environment Variables

Key environment variables (see `.env.example` for complete list):

```bash
# Google AI
GOOGLE_GENAI_USE_VERTEXAI=false
GOOGLE_API_KEY=your-api-key
GOOGLE_CLOUD_PROJECT=your-project

# OAuth (for Google API toolsets)
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# MCP
MCP_STDIO_COMMAND=npx
MCP_SSE_URL=http://localhost:8080/sse

# Services
BIGQUERY_PROJECT=your-project
VERTEX_AI_SEARCH_DATA_STORE_ID=projects/.../dataStores/...
```

## Testing

```bash
# Run demos
python main.py --mode demo --demo sequential
python main.py --mode demo --demo parallel
python main.py --mode demo --demo loop
python main.py --mode demo --demo full

# Interactive testing
python main.py --mode interactive
```

## License

MIT License
