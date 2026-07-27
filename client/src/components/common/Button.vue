<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: 'button' | 'submit' | 'reset'
    variant?: 'default' | 'primary'
  }>(),
  {
    type: 'button',
    variant: 'default',
  },
)

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <button class="sa-button" :class="`sa-button--${variant}`" :type="type" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;

  &--primary {
    border: 1px solid $button-border-primary;
    border-radius: 4px;
    padding: space(1) space(2);
    background: $button-background-primary;

    &:hover {
      background: $button-background-primary-hover;
    }
  }
}
</style>
