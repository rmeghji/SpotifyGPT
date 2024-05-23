<script setup lang="ts">
</script>

<template>
  <div class="container">
    <div class="login-button">
      <button @click="login">Login to Spotify</button>
    </div>
    <div class="main-chat">
      <div v-for="chat in chatHistory" key="chat">
        <p class="user">{{ chat['user'] }}</p>
        <p class="gpt">{{ chat['gpt'] }}</p>
      </div>
      <p class="user">{{ tempInput }}</p>
      <br/>
      <input type="text" v-model="userInput" @keyup.enter="sendMessage" placeholder="Message"/>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios'

// Create custom axios instance for redirecting - used for login
const axiosRedirector = axios.create()
// axiosRedirector.defaults.maxRedirects = 0
axiosRedirector.interceptors.response.use(
  // response => response,
  // error => {
  //   if(error.status == 301 || error.status == 302){
  //     const url = error.response.headers.location
  //     window.location.href = url
  //     return Promise.reject({ canceled: true })
  //     // return axiosRedirector.get(url)
  //   }
  //   return Promise.reject(error)
  // }
  (response) => {
    console.log(response)
    if(response.status == 301 || response.status == 302){
      console.log("301 or 302")
      window.location.href = response.headers.location
      // return Promise.reject({ canceled: true })
      // return axiosRedirector.get(url)
    }
    return response
  },
  (error) => {
    console.log(error)
    console.log(error.request.responseURL)
    // window.location.href = error.request.responseURL
    return Promise.reject(error)
  }
)

export default {
  data() {
    return {
      userInput: '',
      chatResponse: '',
      chatHistory: [{ user: '', gpt: 'Hello! How can I help you today?'}],
      tempInput: ''
    }
  },
  methods: {
    sendMessage() {
      this.tempInput = this.userInput
      axios.post('/SpotifyGPT/api/chat', { input: this.userInput }, { headers: { 'Content-Type': 'application/json' } })
      .then(response => {
        this.chatResponse = response.data.response
        this.tempInput = ''
        this.chatHistory.push({ user: this.userInput, gpt: this.chatResponse })
        this.userInput = ''
      })
      .catch(error => {
        console.error(error)
      })
    },
    login() {
      // window.location.href = '/api/login'
      // axiosRedirector.get('https://spotifygpt-1267e7132268.herokuapp.com/login', { withCredentials: true })
      // axiosRedirector.get('', { withCredentials: true })
      axios.get('/SpotifyGPT/api/login', { withCredentials: true })
      .then(response => {
        // console.log(response)
        window.location.href = response.data.url
        // window.open(response.data.url, '_blank', 'width=800,height=600')
      })
      .catch(error => {
        console.error("weeooo error")
      })
    }
  }
}
</script>

<style scoped>
template {
  align-items: center;
  justify-content: center;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}
input {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px rgb(73, 73, 73);
  border-radius: 0.25rem;
  justify-self: center;
  width: 100%;
  background-color: rgb(70, 70, 70);
}

input::placeholder {
  color: #d2d2d2;
}

.main-chat {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
  max-width: flex;
  max-height: flex;
  flex-grow: 1;
}
.gpt {
  text-emphasis: bold;
  color: #ffffff;
}
.login-button {
  display: flex;
  /* align-self: flex-end; */
  /* justify-content: flex-end; */
}
.login-button button {
  padding: 0.5rem;
  margin: 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.35rem;
  /* justify-self: center; */
}
</style>
