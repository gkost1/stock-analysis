<script setup lang="ts">
defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <button class="sa-button" type="button" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<style scoped lang="scss">
.sa-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;
}
</style>
