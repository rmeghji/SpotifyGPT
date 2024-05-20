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
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      // '/login': {
      //   target: 'https://spotifygpt-1267e7132268.herokuapp.com/login',
      //   changeOrigin: true,
      //   secure: false,
      //   // rewrite: (path) => path.replace(/^\/login/, '/login')
      //   // rewrite: (path) => path.replace(/^\/api/, '')
      // },
      // '/callback': {
      //   target: 'https://spotifygpt-1267e7132268.herokuapp.com/callback',
      //   changeOrigin: true,
      //   secure: false,
      //   // rewrite: (path) => path.replace(/^\/callback/, '/callback')
      //   // rewrite: (path) => path.replace(/^\/api/, '')
      // }
      '/api': {
        target: 'https://spotifygpt-1267e7132268.herokuapp.com',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
