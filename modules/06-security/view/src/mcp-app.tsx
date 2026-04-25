import { useApp } from "@modelcontextprotocol/ext-apps/react";
import { StrictMode, useCallback, useState } from "react";
import { createRoot } from "react-dom/client";
import "./global.css";

interface FridgeItem {
  name: string;
  expiration_date: string;
  category: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  dairy: "#3b82f6",
  vegetable: "#22c55e",
  meat: "#ef4444",
  fruit: "#f59e0b",
  beverage: "#8b5cf6",
  leftover: "#6b7280",
};

const ITEMS_PER_SHELF = 4;

function categoryColor(category: string): string {
  return CATEGORY_COLORS[category.toLowerCase()] ?? "#64748b";
}

function isExpiringSoon(expirationDate: string, days = 3): boolean {
  const expiry = new Date(expirationDate);
  const threshold = new Date();
  threshold.setDate(threshold.getDate() + days);
  return expiry <= threshold;
}

function FridgeApp() {
  const [items, setItems] = useState<FridgeItem[]>([]);

  const { app, error } = useApp({
    appInfo: { name: "Fridge View", version: "1.0.0" },
    capabilities: {},
    onAppCreated: (app) => {
      app.ontoolinput = async (input) => {
        console.info("Received tool input:", input);
      };

      app.ontoolresult = async (result) => {
        console.info("Received tool result:", result);
        const structured = result.structuredContent as Record<string, unknown> | undefined;
        if (structured?.result) {
          const data = structured.result;
          if (Array.isArray(data)) {
            setItems(data as FridgeItem[]);
          }
        }
      };

      app.ontoolcancelled = (params) => {
        console.info("Tool call cancelled:", params.reason);
      };

      app.onerror = console.error;
    },
  });

  const handleOpenRecipes = useCallback(async () => {
    await app?.openLink({ url: "https://www.allrecipes.com/" });
  }, [app]);

  const handleCookSuggestion = useCallback(async () => {
    await app?.sendMessage({
      role: "user",
      content: [{ type: "text", text: "Cook something with the soon expiring ingredients" }],
    });
  }, [app]);

  if (error) return <div className="error">Error: {error.message}</div>;
  if (!app) return <div className="loading">Connecting...</div>;

  const shelves: FridgeItem[][] = [];
  for (let i = 0; i < items.length; i += ITEMS_PER_SHELF) {
    shelves.push(items.slice(i, i + ITEMS_PER_SHELF));
  }

  const usedCategories = [...new Set(items.map((i) => i.category.toLowerCase()))];

  return (
    <div>
      <div className="fridge">
        <div className="fridge-handle" />
        <div className="fridge-header">My Fridge</div>
        {items.length === 0 ? (
          <div className="empty">Fridge is empty</div>
        ) : (
          shelves.map((shelf, si) => (
            <div className="shelf" key={si}>
              {shelf.map((item) => (
                <span
                  key={item.name}
                  className={`item${isExpiringSoon(item.expiration_date) ? " expiring" : ""}`}
                  style={{ background: categoryColor(item.category) }}
                  title={`${item.name} — expires ${item.expiration_date}`}
                >
                  <span className="item-dot" />
                  {item.name}
                </span>
              ))}
            </div>
          ))
        )}
      </div>
      {usedCategories.length > 0 && (
        <div className="legend">
          {usedCategories.map((cat) => (
            <span key={cat} className="legend-item">
              <span className="legend-dot" style={{ background: categoryColor(cat) }} />
              {cat}
            </span>
          ))}
        </div>
      )}
      <div className="actions">
        <button onClick={handleOpenRecipes}>Browse Recipes</button>
        <button onClick={handleCookSuggestion}>Cook with expiring items</button>
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <FridgeApp />
  </StrictMode>,
);
