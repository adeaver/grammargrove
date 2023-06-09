import { defineConfig } from 'vite'
import preact from '@preact/preset-vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [preact()],
  host: true,
  port: 8000,
  watch: {
    usePolling: true,
  },
  build: {
    rollupOptions: {
        output: {
            assetFileNames: "assets/[name].[ext]",
            chunkFileNames: "assets/[name].[ext]",
            entryFileNames: "assets/[name].js",
        },
    },
    write: true,
  },
})
