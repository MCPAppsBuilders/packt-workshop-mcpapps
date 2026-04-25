"""Shared fixtures for MCP server testing.

Uses the FastMCP server's built-in methods directly (no HTTP needed).
"""

import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load .env from the module root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Add the mcp-server source to the path so we can import it directly
MCP_SERVER_DIR = Path(__file__).resolve().parents[2] / "02-architecture" / "mcp-server"
sys.path.insert(0, str(MCP_SERVER_DIR))


@pytest.fixture(scope="session")
def mcp():
    """Import and return the FastMCP server instance."""
    import server as srv
    return srv.mcp
