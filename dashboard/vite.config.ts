import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import { tanstackRouter } from "@tanstack/router-plugin/vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
    }),
    react(),
  ],
  server: {
    port: 5180,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5080",
        changeOrigin: true,
      },
      "/rss": {
        target: "http://127.0.0.1:5080",
        changeOrigin: true,
      },
      "/episodes": {
        target: "http://127.0.0.1:5080",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "../data/dashboard",
  },
})
