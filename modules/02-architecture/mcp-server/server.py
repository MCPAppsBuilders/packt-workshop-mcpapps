import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("basic-math-server", port=8301)

# Patch CORS into the Starlette app (mcp 1.27.0 has no built-in CORS setting)
_original_streamable_http_app = mcp.streamable_http_app

def _patched_streamable_http_app():
    app = _original_streamable_http_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

mcp.streamable_http_app = _patched_streamable_http_app

RESOURCES_DIR = Path(__file__).parent / "resources"


# --- Tools ---


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


# --- Resources ---


@mcp.resource("file://info.txt")
def get_info() -> str:
    """Return the content of the info text file."""
    return (RESOURCES_DIR / "info.txt").read_text()


@mcp.resource("file://config.json")
def get_config() -> str:
    """Return the server configuration as JSON."""
    return (RESOURCES_DIR / "config.json").read_text()


# --- Prompts ---


@mcp.prompt()
def calculate(operation: str = "add", a: str = "0", b: str = "0") -> str:
    """Create a prompt asking the model to perform a calculation."""
    return f"Please use the {operation} tool with a={a} and b={b}, and explain the result."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
