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
        // { path: `/callback`, component: App, async beforeEnter(to: any, from: any, next: any) {
        //     try {
        //         const response = await axios.post('https://spotifygpt-1267e7132268.herokuapp.com/callback',
        //             { code: to.query.code }, { responseType: 'json', withCredentials: true },)
        //         next(`/`)
        //     }
        //     catch(err) {
        //         console.error(err)
        //         next(`/`)
        //     }
        // }}
    ],
})

const app = createApp(App)
app.use(router)
app.mount('#app')