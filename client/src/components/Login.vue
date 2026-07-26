<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ authenticated: [token: string] }>()
const mode = ref<'login' | 'register'>('login')
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function submit() {
  error.value = ''
  const path = mode.value === 'login' ? 'auth/login' : 'auth/register'
  const body =
    mode.value === 'login'
      ? { username: username.value, password: password.value }
      : { username: username.value, email: email.value, password: password.value }

  const response = await fetch(`http://localhost:8000/core/${path}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    error.value = data.detail ?? 'Something went wrong. Please try again.'
    return
  }

  const data = await response.json()
  emit('authenticated', data.token)
}
</script>

<template>
  <form class="login" @submit.prevent="submit">
    <h1>{{ mode === 'login' ? 'Log in' : 'Create an account' }}</h1>

    <label>
      Username
      <input v-model="username" type="text" required autocomplete="username" />
    </label>

    <label v-if="mode === 'register'">
      Email
      <input v-model="email" type="email" required autocomplete="email" />
    </label>

    <label>
      Password
      <input
        v-model="password"
        type="password"
        required
        :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"
      />
    </label>

    <p v-if="error" class="error">{{ error }}</p>

    <button type="submit">{{ mode === 'login' ? 'Log in' : 'Create account' }}</button>

    <p class="toggle">
      <template v-if="mode === 'login'">
        Don't have an account?
        <a href="#" @click.prevent="mode = 'register'">Sign up</a>
      </template>
      <template v-else>
        Already have an account?
        <a href="#" @click.prevent="mode = 'login'">Log in</a>
      </template>
    </p>
  </form>
</template>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 20rem;
  margin: 4rem auto;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.9rem;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
}

button {
  padding: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
}

.error {
  color: crimson;
  font-size: 0.9rem;
}

.toggle {
  font-size: 0.85rem;
  text-align: center;
}
</style>
