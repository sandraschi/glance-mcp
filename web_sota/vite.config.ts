import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
  server: {
    port: 10777,
    host: "127.0.0.1",
    proxy: {
      "/api": { target: "http://127.0.0.1:10776", changeOrigin: true },
      "/health": { target: "http://127.0.0.1:10776", changeOrigin: true },
      "/docs": { target: "http://127.0.0.1:10776", changeOrigin: true },
    },
  },
});
