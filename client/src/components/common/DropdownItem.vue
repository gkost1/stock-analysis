<template>
  <button class="sa-dropdown-item" type="button" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-dropdown-item {
  display: block;
  width: 100%;
  padding: space(2) space(4);
  border: none;
  background: none;
  color: inherit;
  font: inherit;
  text-align: left;
  cursor: pointer;

  &:hover {
    background-color: $gray-800;
  }
}
</style>
