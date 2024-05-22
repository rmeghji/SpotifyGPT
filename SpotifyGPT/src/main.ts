import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: App },
        { path: '/callback', async beforeEnter(to: any, from: any, next: any) {
            try {
                if(to.method === 'GET') {
                    const response = await axios.post('/api/callback', { 'code': new URLSearchParams(location.search).get('code') })
                    console.log(response.data.login_status)
                }
                next('/')
            }
            catch(err) {
                console.error(err)
                next('/')
            }
        }}
    ],
})

createApp(App).mount('#app')