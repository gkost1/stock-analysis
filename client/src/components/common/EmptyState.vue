<template>
  <p class="sa-empty-state">{{ message }}</p>
</template>

<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>


<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-empty-state {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  color: $font-color-default;
}
</style>
