import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: `/`, component: App },
        { path: `/callback`, component: App, async beforeEnter(to: any, from: any, next: any) {
            try {
                const response = await axios.post('/api/callback',
                    { code: to.query.code })
                next(`/`)
            }
            catch(err) {
                console.error(err)
                next(`/`)
            }
        }}
    ],
})

const app = createApp(App)
app.use(router)
app.mount('#app')