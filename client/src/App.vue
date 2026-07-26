<script setup lang="ts">
import { ref } from 'vue'
import Login from './components/Login.vue'

const token = ref<string | null>(localStorage.getItem('token'))

function onAuthenticated(newToken: string) {
  localStorage.setItem('token', newToken)
  token.value = newToken
}

function logout() {
  localStorage.removeItem('token')
  token.value = null
}
</script>

<template>
  <Login v-if="!token" @authenticated="onAuthenticated" />
  <div v-else>
    <h1>You're logged in!</h1>
    <button @click="logout">Log out</button>
  </div>
</template>

<style scoped></style>
