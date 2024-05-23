import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: `/`, component: App, async beforeEnter(to: any, from: any, next: any){
            console.log("beforeEnter")
            try {
                // const response = await axios.post('https://spotifygpt-1267e7132268.herokuapp.com/callback',
                //     { code: to.query.code })
                // next(`/${import.meta.env.BASE_URL}`)
                const urlParams = new URLSearchParams(window.location.search);
                console.log(urlParams);
                const code = urlParams.get('code');
                console.log(code);

                if (code) {
                    await axios.post('https://spotifygpt-1267e7132268.herokuapp.com/callback', { code: code });
                    // next(`/${import.meta.env.BASE_URL}/`);
                }
                next(`/`);
            }
            catch(err) {
                console.error(err)
                next(`/`)
            }
        }},
        { path: `/callback`, component: App, async beforeEnter(to: any, from: any, next: any) {
            try {
                // const response = await axios.post('/api/callback',
                //     { code: to.query.code })
                const response = await axios.post('https://spotifygpt-1267e7132268.herokuapp.com/callback',
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