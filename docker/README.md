# Workshop Docker stack

Everything you need to follow the workshop, in two containers:

| Service    | URL                     | What it is                          |
|------------|-------------------------|-------------------------------------|
| `workshop` | http://localhost:8443   | VSCode in the browser (code-server) |
| `keycloak` | http://localhost:8080   | OAuth 2.1 server for Module 6       |

The `workshop` container ships Python 3.11, Node.js 24, `ngrok`, the MCP
Inspector, MCP Jam, FastMCP, and a pre-wired `/data` volume so every file
you create survives restarts and exports cleanly.

## Prerequisites

Docker Desktop (macOS/Windows) or Docker Engine + Compose plugin (Linux).

## First run

```bash
cd fridge-manager/docker
cp .env.example .env          # edit if you want to change the VSCode password
mkdir -p data                 # workspace that will be bind-mounted into /data
docker compose up --build     # first build takes a few minutes
```

Then open:

1. http://localhost:8443 and log in with the password from `.env`
   (default `mcpapps`). You are now inside VSCode, in `/data`.
2. http://localhost:8080 for Keycloak (admin / admin). The `mcp` realm
   is pre-imported with a `fridge-manager` OAuth 2.1 client and a `demo`
   user (password `demo`).

## Inside the workshop container

From the VSCode terminal:

```bash
python --version                           # 3.11+
node --version                             # 24.x
ngrok --version                            # installed, token optional

# Run the MCP Inspector (stdio debug UI)
npx @modelcontextprotocol/inspector

# Run MCP Jam (browser host that mounts ui:// resources)
npx @mcpjam/cli

# Boot the fridge FastMCP server in HTTP mode (module 3 onwards)
python server/app.py --transport streamable-http --port 8000

# Start the React view
cd view && npm install && npm run dev -- --host 0.0.0.0 --port 5173
```

To expose the local server to ChatGPT during the live demo:

```bash
ngrok config add-authtoken <your-ngrok-token>   # once
ngrok http 8000
```

## Ports exposed by the stack

| Port | Service                                      |
|------|----------------------------------------------|
| 8080 | Keycloak                                     |
| 8443 | code-server (VSCode web)                     |
| 8000 | FastMCP Python server                        |
| 5173 | Vite dev server for the React view           |
| 4040 | ngrok local inspector                        |

## Exporting your work

Everything lives in `./data` on your host. Zip that folder and you have
the full workshop output (server, view, notes, SQLite DB, etc.).

```bash
tar czf fridge-workshop-$(date +%Y%m%d).tgz data
```

## Cleaning up

```bash
docker compose down             # stop
docker compose down -v          # stop + drop Keycloak volume (reimport on next up)
```

The `./data` folder is never deleted by `docker compose down` because it
is a bind mount, so your work is safe.

## Troubleshooting

- **Keycloak returns 401 on first boot**: it is still importing the realm.
  Wait 10-15 seconds and reload.
- **code-server asks for a password but yours does not work**: the
  `PASSWORD` env variable must be set before `docker compose up`. Edit
  `.env` and run `docker compose up -d --force-recreate workshop`.
- **`ngrok http 8000` says "authentication required"**: run
  `ngrok config add-authtoken <your-token>` inside the VSCode terminal.
