<script setup lang="ts">
import { onMounted, onUnmounted, useTemplateRef } from 'vue'

const open = defineModel<boolean>('open', { default: false })

const menuRef = useTemplateRef('menuRef')

function isClickInsideMenuRef(event: MouseEvent){
  return menuRef.value && menuRef.value.contains(event.target as Node)
}

function onClickOutside(event: MouseEvent) {
  if (open.value && menuRef.value && !isClickInsideMenuRef(event)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div v-if="open" ref="menuRef" class="sa-dropdown-menu">
    <slot />
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  min-width: 160px;
  margin-top: space(1);
  padding: space(1) 0;
  background-color: $surface-background-default;
  border: 1px solid $surface-border-default;
}
</style>
