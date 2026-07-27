<template>
  <div class="sa-card">
    <slot />
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-card {
  height: 20vh;
  padding: space(2) space(4) space(4);
  background-color: $surface-background-secondary;
  border: 1px solid transparent;
  border-radius: 4px;
}
</style>
