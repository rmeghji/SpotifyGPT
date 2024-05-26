import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Chat from './Chat.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: `/`, component: App },
        { path: `/callback`, component: Chat }
    ],
})

const app = createApp(App)
app.use(router)
app.component('chat', Chat)
app.mount('#app')