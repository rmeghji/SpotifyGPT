import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  base: '/SpotifyGPT',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/SpotifyGPT/api': {
        target: 'https://spotifygpt-1267e7132268.herokuapp.com',
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '')
        rewrite: (path) => path.replace(/^\/SpotifyGPT\/api/, '')

      }
    }
  }
})
