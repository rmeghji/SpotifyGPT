import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: `/`, component: () => import('./Login.vue') },
        { path: `/chat`, component: () => import('./Chat.vue') },
        { path: `/callback`, component: () => import('./Callback.vue') },
    ],
})

const app = createApp(App)
app.use(router)
app.mount('#app')