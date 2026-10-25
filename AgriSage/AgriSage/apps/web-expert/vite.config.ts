import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { fileURLToPath, URL } from 'node:url';

const configuredBasePath = process.env.VITE_BASE_PATH?.trim() || '/';
const base = configuredBasePath === '/'
  ? '/'
  : `/${configuredBasePath.replace(/^\/+|\/+$/g, '')}/`;

// https://vite.dev/config/
export default defineConfig({
  // Local builds use the site root. GitHub Pages supplies VITE_BASE_PATH=/AgriSage/.
  // This keeps BrowserRouter and every public asset URL on the same deployment path.
  base,
  plugins: [
    react(),
    tailwindcss()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
    dedupe: ['react', 'react-dom']
  }
});
