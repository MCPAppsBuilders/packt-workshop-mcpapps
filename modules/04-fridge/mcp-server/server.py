import json
from datetime import date, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP(
    "fridge-server",
    port=8304,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

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

FRIDGE_FILE = Path(__file__).parent / "fridge.json"
ASSETS_DIR = Path(__file__).parent / "assets"

FRIDGE_UI_URI = "ui://fridge/fridge.html"


def _load() -> list[dict]:
    return json.loads(FRIDGE_FILE.read_text())


def _save(items: list[dict]) -> None:
    FRIDGE_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False))


# --- Tools ---


@mcp.tool(meta={"ui": {"resourceUri": FRIDGE_UI_URI}})
def list_fridge_contents() -> list[dict]:
    """List all items currently in the fridge."""
    return _load()


@mcp.tool(meta={"ui": {"resourceUri": FRIDGE_UI_URI}})
def add_item(name: str, expiration_date: str, category: str) -> dict:
    """Add an item to the fridge.

    Args:
        name: Name of the item (e.g. "milk", "tomatoes").
        expiration_date: Expiration date in YYYY-MM-DD format.
        category: Category of the item (e.g. "dairy", "vegetable", "meat", "fruit", "beverage", "leftover").
    """
    item = {"name": name, "expiration_date": expiration_date, "category": category}
    items = _load()
    items.append(item)
    _save(items)
    return item


@mcp.tool(meta={"ui": {"resourceUri": FRIDGE_UI_URI}})
def remove_item(name: str) -> str:
    """Remove an item from the fridge by name.

    Args:
        name: Name of the item to remove.
    """
    items = _load()
    updated = [i for i in items if i["name"].lower() != name.lower()]
    if len(updated) == len(items):
        return f"Item '{name}' not found in the fridge."
    _save(updated)
    return f"Removed '{name}' from the fridge."


@mcp.tool(meta={"ui": {"resourceUri": FRIDGE_UI_URI}})
def expiring_soon(days: int = 3) -> list[dict]:
    """List items expiring within the given number of days.

    Args:
        days: Number of days to look ahead (default: 3).
    """
    items = _load()
    threshold = date.today() + timedelta(days=days)
    return [i for i in items if date.fromisoformat(i["expiration_date"]) <= threshold]


# --- Resources ---


@mcp.resource("file://fridge.json", mime_type="application/json")
def get_fridge() -> str:
    """Return the raw fridge contents as JSON."""
    return FRIDGE_FILE.read_text()


@mcp.resource(
    uri=FRIDGE_UI_URI,
    mime_type="text/html;profile=mcp-app",
    meta={"ui": {"prefersBorder": False}},
)
def get_fridge_widget() -> str:
    """Return the fridge interactive widget HTML."""
    return (ASSETS_DIR / "fridge.html").read_text()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
