"""
Database integrations for Google ADK.

Provides configurations for database connections:
- MCP Toolbox for Databases (30+ data sources)
- Vector databases (Qdrant, Chroma)
- Document databases (MongoDB)
- Cloud databases (BigQuery, Spanner, Bigtable)
"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from google.adk.tools.toolbox_toolset import ToolboxToolset


# =============================================================================
# MCP Toolbox for Databases Configuration
# =============================================================================

@dataclass
class ToolboxDatabaseConfig:
    """
    Configuration for MCP Toolbox for Databases.
    
    MCP Toolbox supports 30+ data sources including:
    
    Google Cloud:
        - BigQuery, AlloyDB, Spanner, Cloud SQL (PostgreSQL, MySQL, SQL Server)
        - Firestore, Bigtable, Dataplex, Cloud Monitoring
    
    Relational:
        - PostgreSQL, MySQL, SQL Server, ClickHouse, TiDB
        - OceanBase, Firebird, SQLite, YugabyteDB
    
    NoSQL:
        - MongoDB, Couchbase, Redis, Valkey, Cassandra
    
    Graph:
        - Neo4j, Dgraph
    
    Data Platforms:
        - Looker, Trino
    """
    server_url: str = "http://127.0.0.1:5000"
    toolset_name: Optional[str] = None
    tool_names: Optional[List[str]] = None
    
    def __post_init__(self):
        self.server_url = os.getenv("TOOLBOX_SERVER_URL", self.server_url)


toolbox_database_config = ToolboxDatabaseConfig()


def get_toolbox_database_toolset(
    server_url: Optional[str] = None,
    toolset_name: Optional[str] = None,
    tool_names: Optional[List[str]] = None,
    credentials: Optional[Any] = None,
    bound_params: Optional[Dict[str, Any]] = None,
) -> ToolboxToolset:
    """
    Get MCP Toolbox for Databases toolset.
    
    MCP Toolbox provides enterprise-grade database connectivity for AI agents.
    
    Args:
        server_url: Toolbox server URL.
        toolset_name: Specific toolset to load.
        tool_names: Specific tools to load.
        credentials: Authentication credentials.
        bound_params: Parameters to bind to tools.
    
    Returns:
        ToolboxToolset: Configured database toolset.
    
    Example:
        # Connect to all databases
        toolset = get_toolbox_database_toolset()
        
        # Connect to specific toolset
        toolset = get_toolbox_database_toolset(toolset_name="bigquery")
        
        # With bound parameters
        toolset = get_toolbox_database_toolset(
            bound_params={"project_id": "my-project"}
        )
    """
    return ToolboxToolset(
        server_url=server_url or os.getenv("TOOLBOX_SERVER_URL", "http://127.0.0.1:5000"),
        toolset_name=toolset_name,
        tool_names=tool_names,
        credentials=credentials,
        bound_params=bound_params,
    )


# =============================================================================
# Qdrant Vector Database Configuration
# =============================================================================

@dataclass
class QdrantConfig:
    """Configuration for Qdrant vector database."""
    host: str = "localhost"
    port: int = 6333
    api_key: Optional[str] = None
    collection_name: str = "default"
    
    def __post_init__(self):
        self.host = os.getenv("QDRANT_HOST", self.host)
        self.api_key = self.api_key or os.getenv("QDRANT_API_KEY")


def get_qdrant_config(
    host: str = "localhost",
    port: int = 6333,
    api_key: Optional[str] = None,
    collection_name: str = "default",
) -> QdrantConfig:
    """
    Get Qdrant configuration.
    
    Qdrant is a vector similarity search engine for AI applications.
    
    Args:
        host: Qdrant server host.
        port: Qdrant server port.
        api_key: Optional API key for cloud deployment.
        collection_name: Default collection name.
    
    Returns:
        QdrantConfig: Configuration object.
    
    Usage with ADK:
        # Use with Vertex AI RAG or custom tools
        config = get_qdrant_config()
    """
    return QdrantConfig(
        host=host,
        port=port,
        api_key=api_key,
        collection_name=collection_name,
    )


# =============================================================================
# Chroma Vector Database Configuration
# =============================================================================

@dataclass
class ChromaConfig:
    """Configuration for Chroma vector database."""
    host: str = "localhost"
    port: int = 8000
    collection_name: str = "default"
    persist_directory: Optional[str] = None
    
    def __post_init__(self):
        self.host = os.getenv("CHROMA_HOST", self.host)


def get_chroma_config(
    host: str = "localhost",
    port: int = 8000,
    collection_name: str = "default",
    persist_directory: Optional[str] = None,
) -> ChromaConfig:
    """
    Get Chroma configuration.
    
    Chroma is an open-source embedding database.
    
    Args:
        host: Chroma server host.
        port: Chroma server port.
        collection_name: Default collection name.
        persist_directory: Directory for persistent storage.
    
    Returns:
        ChromaConfig: Configuration object.
    """
    return ChromaConfig(
        host=host,
        port=port,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )


# =============================================================================
# MongoDB Configuration
# =============================================================================

@dataclass
class MongoDBConfig:
    """Configuration for MongoDB."""
    connection_string: str = "mongodb://localhost:27017"
    database: str = "default"
    collection: str = "default"
    
    def __post_init__(self):
        self.connection_string = os.getenv("MONGODB_URI", self.connection_string)


def get_mongodb_config(
    connection_string: Optional[str] = None,
    database: str = "default",
    collection: str = "default",
) -> MongoDBConfig:
    """
    Get MongoDB configuration.
    
    MongoDB is a document database for AI applications.
    
    Args:
        connection_string: MongoDB connection URI.
        database: Database name.
        collection: Collection name.
    
    Returns:
        MongoDBConfig: Configuration object.
    """
    return MongoDBConfig(
        connection_string=connection_string or os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        database=database,
        collection=collection,
    )


# =============================================================================
# Cloud Database Configurations
# =============================================================================

@dataclass
class SpannerConfig:
    """Configuration for Google Cloud Spanner."""
    project: Optional[str] = None
    instance: Optional[str] = None
    database: Optional[str] = None
    dialect: str = "GoogleSQL"  # or "PostgreSQL"
    
    def __post_init__(self):
        self.project = self.project or os.getenv("GOOGLE_CLOUD_PROJECT")


@dataclass
class BigtableConfig:
    """Configuration for Google Cloud Bigtable."""
    project: Optional[str] = None
    instance: Optional[str] = None
    table: Optional[str] = None
    
    def __post_init__(self):
        self.project = self.project or os.getenv("GOOGLE_CLOUD_PROJECT")
