import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";
import { rename } from "node:fs/promises";
import { join } from "node:path";

function renameHtml(outDir: string, newName: string): Plugin {
  return {
    name: "rename-html",
    closeBundle: async () => {
      await rename(join(outDir, "index.html"), join(outDir, newName));
    },
  };
}

const outDir = "../mcp-server/assets";

export default defineConfig({
  plugins: [react(), viteSingleFile(), renameHtml(outDir, "basic_add.html")],
  build: {
    outDir,
    emptyOutDir: false,
  },
});
