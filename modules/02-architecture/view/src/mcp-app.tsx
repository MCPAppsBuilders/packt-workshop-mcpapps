import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { useApp } from "@modelcontextprotocol/ext-apps/react";
import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./global.css";

interface ToolInput {
  a?: number;
  b?: number;
}

function MathApp() {
  const [toolInput, setToolInput] = useState<ToolInput | null>(null);
  const [toolResult, setToolResult] = useState<CallToolResult | null>(null);

  const { app, error } = useApp({
    appInfo: { name: "Math View", version: "1.0.0" },
    capabilities: {},
    onAppCreated: (app) => {
      app.ontoolinput = async (input) => {
        console.info("Received tool input:", input);
        if (input.arguments) {
          setToolInput(input.arguments as ToolInput);
        }
      };

      app.ontoolresult = async (result) => {
        console.info("Received tool result:", result);
        setToolResult(result);
      };

      app.ontoolcancelled = (params) => {
        console.info("Tool call cancelled:", params.reason);
      };

      app.onerror = console.error;
    },
  });

  if (error) return <div className="error">Error: {error.message}</div>;
  if (!app) return <div className="loading">Connecting...</div>;

  const a = toolInput?.a ?? "—";
  const b = toolInput?.b ?? "—";
  const structured = toolResult?.structuredContent as Record<string, unknown> | undefined;
  const result = String(structured?.result ?? "—");

  return (
    <main>
      <h1>Math Operation</h1>
      <div className="card">
        <div className="row">
          <span className="label">A</span>
          <span className="value">{String(a)}</span>
        </div>
        <div className="row">
          <span className="label">B</span>
          <span className="value">{String(b)}</span>
        </div>
        <hr />
        <div className="row result">
          <span className="label">A + B</span>
          <span className="value">{result}</span>
        </div>
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MathApp />
  </StrictMode>,
);
