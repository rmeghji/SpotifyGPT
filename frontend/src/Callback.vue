<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<template>
    <div class="container">
        <header>
            <h1>Redirecting...</h1>
            <h4>If you aren't redirected to the chat interface, click</h4> <RouterLink to="/chat">here</RouterLink> <h4>.</h4>
        </header>
    </div>
</template>

<script lang="ts">
import axios from 'axios'

export default {
    created(this: any) {
        console.log('callback')
        try {
            const { code } = this.$route.query;
            axios.post(
                'https://spotifygpt-1267e7132268.herokuapp.com/callback',
                { code: code },
                { responseType: 'json', withCredentials: true, headers: { 'Content-Type': 'application/json' } }
            )
            .then(response => {
                console.log(response)
                // axios.post('https://spotifygpt-1267e7132268.herokuapp.com/chat', { input: 'hello' }, { headers: { 'Content-Type': 'application/json' }, withCredentials: true })
                // .then(response => {
                //     const chatResponse = response.data.response
                //     console.log(chatResponse)
                // })
                // .catch(error => {
                //     console.error(error)
                // })
                axios.get('https://spotifygpt-1267e7132268.herokuapp.com/test', { headers: { 'Content-Type': 'application/json' }, withCredentials: true })
                .then(response => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.error(error)
                })
                this.$router.push({ path: '/chat'})
            })
            .catch(error => {
                console.error(error)
                this.$router.push({ path: '/' })
            })
        }
        catch(err) {
            console.error(err)
        }
    },
}

</script>