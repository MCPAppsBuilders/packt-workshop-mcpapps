# -----------------------------------------------------------------------------
# Workshop image: Python 3.11, Node 24, ngrok, MCP tooling, and code-server.
#
# The participant connects to http://localhost:8443, opens the built-in
# terminal, and runs everything inside /data which is a bind-mounted volume.
# -----------------------------------------------------------------------------
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# -----------------------------------------------------------------------------
# System packages + Python toolchain
# -----------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl wget gnupg git sudo \
        build-essential pkg-config \
        python3 python3-pip python3-venv \
        jq vim less procps lsof \
    && ln -sf /usr/bin/python3 /usr/local/bin/python \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Node.js 24 (NodeSource)
# -----------------------------------------------------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && node --version \
    && npm --version

# -----------------------------------------------------------------------------
# ngrok client (official apt repo)
# -----------------------------------------------------------------------------
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
        | gpg --dearmor -o /etc/apt/keyrings/ngrok.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/ngrok.gpg] https://ngrok-agent.s3.amazonaws.com bookworm main" \
        > /etc/apt/sources.list.d/ngrok.list \
    && apt-get update && apt-get install -y --no-install-recommends ngrok \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# code-server (VSCode in the browser)
# -----------------------------------------------------------------------------
RUN curl -fsSL https://code-server.dev/install.sh | sh

# -----------------------------------------------------------------------------
# Python MCP stack (FastMCP + MCP CLI)
# -----------------------------------------------------------------------------
RUN pip install --no-cache-dir "mcp[cli]" fastmcp

# -----------------------------------------------------------------------------
# MCP test tooling (Inspector + MCP Jam)
# -----------------------------------------------------------------------------
RUN npm install -g \
        @modelcontextprotocol/inspector \
        @mcpjam/cli \
    && npm cache clean --force

# -----------------------------------------------------------------------------
# Workspace: single /data volume, exportable from the host
# -----------------------------------------------------------------------------
RUN mkdir -p /data && chmod 777 /data
WORKDIR /data
VOLUME /data

# Pre-install a few handy VSCode extensions for the workshop
RUN code-server --install-extension ms-python.python \
    && code-server --install-extension esbenp.prettier-vscode \
    && code-server --install-extension dbaeumer.vscode-eslint \
    && code-server --install-extension redhat.vscode-yaml

# Copy the entrypoint that authenticates ngrok if a token is provided,
# then hands off to code-server.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# code-server web UI
EXPOSE 8443
# FastMCP Python server (HTTP/SSE transport)
EXPOSE 8000
# Vite dev server for the React view
EXPOSE 5173
# ngrok local inspector
EXPOSE 4040

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
