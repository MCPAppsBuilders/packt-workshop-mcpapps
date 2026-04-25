# Module 04 - Fridge

MCP server to manage the contents of a fridge. Items are persisted in `fridge.json`.

## Structure

```
04-fridge/
├── mcp-server/      # Python MCP server (FastMCP + uv)
│   ├── server.py    # 4 tools, 1 resource
│   └── fridge.json  # Persisted fridge contents
└── view/            # (future) Interactive UI
```

## Tools

| Tool | Description |
|------|-------------|
| `list_fridge_contents` | List all items in the fridge |
| `add_item(name, expiration_date, category)` | Add an item |
| `remove_item(name)` | Remove an item by name |
| `expiring_soon(days=3)` | List items expiring within N days |

Each item has: **name**, **expiration_date** (YYYY-MM-DD), **category**.

## Resource

- `file://fridge.json` — raw fridge contents

## Run

```bash
cd mcp-server
uv run python server.py
```
