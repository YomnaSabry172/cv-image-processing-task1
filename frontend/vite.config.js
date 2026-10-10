// Owner: Lead — Vite config (React + Tailwind)
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    strictPort: true, // the backend's CORS only allows :5173, so never silently move to another port
  },
})
