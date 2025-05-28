/// <reference types="vitest" />

import legacy from '@vitejs/plugin-legacy'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@forward "@/theme/variables.scss";`
      }
    }
  },
  server: {
    proxy: {
      '/api': 'http://0.0.0.0:8000',
      '/graphql': 'http://0.0.0.0:8000',
    },
    port: 8000
  },
  test: {
    globals: true,
    environment: 'jsdom'
  }
})
