#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Workshop container entrypoint.
# 1. Wire up ngrok if a token is provided.
# 2. Start code-server bound to all interfaces on port 8443.
# -----------------------------------------------------------------------------

if [ -n "${NGROK_AUTHTOKEN:-}" ]; then
    echo "[entrypoint] configuring ngrok with provided authtoken"
    ngrok config add-authtoken "${NGROK_AUTHTOKEN}" || true
else
    echo "[entrypoint] NGROK_AUTHTOKEN is empty."
    echo "              Run: ngrok config add-authtoken <your-token>"
    echo "              from the VSCode terminal once you have signed up."
fi

# Friendly welcome in /data the first time the container boots.
if [ ! -f /data/README.md ]; then
    cat > /data/README.md <<'EOF'
# MCP Apps workshop workspace

This folder is mounted from your host machine, so everything you write here
survives container restarts and can be exported as-is.

Suggested layout:

    /data
      server/     # Python FastMCP server (fridge-manager)
      view/       # React view for the MCP App
      auth/       # Keycloak realm exports / OAuth scratchpad

Quick commands:

    python --version         # Python 3.11+
    node --version           # Node.js 24
    ngrok --version          # ngrok client

    npx @modelcontextprotocol/inspector   # Debug tools over stdio
    npx @mcpjam/cli                       # Run an MCP host in the browser

Keycloak is reachable at http://keycloak:8080 from inside the container
(and http://localhost:8080 from your host).
EOF
fi

echo "[entrypoint] starting code-server on 0.0.0.0:8443 (password auth)"
exec code-server \
    --bind-addr 0.0.0.0:8443 \
    --auth password \
    --disable-telemetry \
    /data
