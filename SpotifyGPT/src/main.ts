import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: App },
        { path: '/callback', component: App, async beforeEnter(to: any, from: any, next: any) {
            try {
                console.log(to)
                console.log(to.query.code)
                const response = await axios.post('/api/callback', { 'code': new URLSearchParams(to.query.code) })
                console.log(response.data.login_status)
                next('/')
            }
            catch(err) {
                console.error(err)
                next('/')
            }
        }}
    ],
})

const app = createApp(App)
app.use(router)
app.mount('#app')