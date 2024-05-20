<script setup lang="ts">
</script>

<template>
  <div class="main-chat">
    <div v-for="chat in chatHistory" :key="chat">
      <p class="user">{{ chat['user'] }}</p>
      <p class="gpt">{{ chat['gpt'] }}</p>
    </div>
    <p class="user">{{ tempInput }}</p>
    <br/>
    <input type="text" v-model="userInput" @keyup.enter="sendMessage" placeholder="Message"/>
  </div>
</template>

<script lang="ts">
import axios from 'axios'

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

      axios.post('https://spotifygpt-1267e7132268.herokuapp.com/', { input: this.userInput })
      .then(response => {
        this.chatResponse = response.data.response
        this.tempInput = ''
        this.chatHistory.push({ user: this.userInput, gpt: this.chatResponse })
        this.userInput = ''
      })
      .catch(error => {
        console.error(error)
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
input {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  justify-self: center;
  width: 100%;
}
.main-chat {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
  max-width: flex;
}
.gpt {
  text-emphasis: bold;
  color: #ffffff;
}
</style>
