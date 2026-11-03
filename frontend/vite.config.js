import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// The backend (FastAPI) already sends permissive CORS headers
// (see app/main.py -> CORSMiddleware allow_origins=["*"]), so calling it
// directly by full URL (VITE_API_BASE_URL) works with zero extra setup.
//
// This proxy is kept as an optional second path for local development:
// if you set VITE_API_BASE_URL="/api" in .env, every request from the
// React app to "/api/..." is transparently forwarded by Vite's dev server
// to BACKEND_ORIGIN below, so the browser never makes a cross-origin
// request at all during `npm run dev`.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const BACKEND_ORIGIN = env.VITE_BACKEND_ORIGIN || "http://127.0.0.1:8000";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: BACKEND_ORIGIN,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
        "/static": {
          target: BACKEND_ORIGIN,
          changeOrigin: true,
        },
      },
    },
  };
});
