// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    //Outputs directly to Django's static folder.
    outDir: path.resolve(__dirname, '../static/snake'),
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: 'snake-bundle.js',
        assetFileNames: 'snake-style.[ext]',
      },
    },
  },
})