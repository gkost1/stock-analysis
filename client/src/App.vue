<template>
  <Login v-if="!token" @authenticated="onAuthenticated" />
  <div v-else>
    <TopBar />
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Login from './components/Login.vue'
import TopBar from './components/common/TopBar.vue'

const router = useRouter()
const token = ref<string | null>(localStorage.getItem('token'))

function onAuthenticated(newToken: string) {
  localStorage.setItem('token', newToken)
  token.value = newToken
  router.push('/simulations')
}

function logout() {
  localStorage.removeItem('token')
  token.value = null
}
</script>

<style scoped></style>
