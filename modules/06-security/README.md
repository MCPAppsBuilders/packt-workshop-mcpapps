# Module 06 - Security (OAuth 2.1 with Keycloak)

MCP Fridge Server secured with OAuth 2.1 using Keycloak as the authorization server. JWT tokens are validated locally using the Keycloak JWKS endpoint.

## Architecture

```
Client  ──Bearer token──>  MCP Server (port 9306)
                              │
                              ├── validates JWT signature via JWKS
                              └── checks issuer, audience, expiration

Keycloak (port 8080)  ──issues tokens──>  Client
```

## Structure

```
06-security/
├── mcp-server/
│   ├── server.py            # MCP server with OAuth 2.1 auth
│   ├── token_verifier.py    # Keycloak JWT verifier
│   ├── fridge.json          # Persisted fridge contents
│   └── pyproject.toml
├── keycloak/
│   └── realm-export.json    # Auto-imported realm config
├── docker-compose.yml       # Keycloak service
└── view/                    # Interactive UI
```

## Setup

### 1. Start Keycloak

```bash
docker compose up -d
```

Keycloak admin console: http://localhost:8080 (admin / admin)

The `mcp` realm is auto-imported with:
- **Client** `mcp-fridge-server` (confidential, PKCE required)
- **Client** `mcp-client` (public, PKCE required)
- **User** `testuser` / `testpassword`

### 2. Start the MCP server

```bash
cd mcp-server
uv sync
uv run python server.py
```

Server runs on http://localhost:9306 — all endpoints require a valid Bearer token.

### 3. Get a token and test

```bash
# Get a token via Resource Owner Password (for testing)
TOKEN=$(curl -s -X POST http://localhost:8080/realms/mcp/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=mcp-fridge-server" \
  -d "client_secret=mcp-fridge-secret" \
  -d "username=testuser" \
  -d "password=testpassword" \
  -d "scope=openid" | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo $TOKEN

# Test the MCP server (should succeed with valid token)
curl -X POST http://localhost:9306/mcp/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

## What changed vs module 04

| File | Change |
|------|--------|
| `server.py` | Added `AuthSettings` + `token_verifier` to `FastMCP` |
| `token_verifier.py` | **New** — validates Keycloak JWTs via JWKS |
| `pyproject.toml` | Added `pyjwt[crypto]` dependency |
| `docker-compose.yml` | **New** — Keycloak service |
| `keycloak/realm-export.json` | **New** — realm with clients and test user |
