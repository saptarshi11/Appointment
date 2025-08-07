import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
  server: {
    proxy: {
      "/api": {
        target: process.env.NODE_ENV === 'production' 
          ? "https://your-backend-url.vercel.app" 
          : "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
