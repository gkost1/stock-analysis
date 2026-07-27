<script setup lang="ts">
defineEmits<{
  submit: []
}>()
</script>

<template>
  <form class="sa-form" @submit.prevent="$emit('submit')">
    <slot />
  </form>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-form {
  display: flex;
  flex-direction: column;
  gap: space(4);
}
</style>
