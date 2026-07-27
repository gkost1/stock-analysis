<template>
  <p class="sa-loading-state">
    <span>{{ message }}</span><span class="sa-loading-state__dots">{{ dots }}</span>
  </p>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

defineProps<{
  message: string
}>()

const dotsCount = ref(1)
const dots = computed(() => '.'.repeat(dotsCount.value))
let interval: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  interval = setInterval(() => {
    dotsCount.value = (dotsCount.value % 3) + 1
  }, 500)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-loading-state {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  color: $font-color-default;

  &__dots {
    display: inline-block;
    width: 3ch;
    text-align: left;
  }
}
</style>
