<script setup lang="ts">
import Button from './Button.vue'
import Icon from './Icon.vue'

const open = defineModel<boolean>('open', { default: false })

withDefaults(
  defineProps<{
    width?: 'xs' | 's' | 'm' | 'l' | 'xl'
  }>(),
  {
    width: 'm',
  },
)

function close() {
  open.value = false
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="sa-modal-overlay" @click.self="close">
      <div class="sa-modal" :class="`sa-modal--${width}`">
        <Button class="sa-modal__close" @click="close">
          <Icon name="close" />
        </Button>
        <slot />
      </div>
    </div>
  </Teleport>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.6);
}

.sa-modal {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  padding: space(6);
  background-color: $surface-background-secondary;
  border: 1px solid $surface-border-default;

  &--xs {
    width: 20vw;
  }

  &--s {
    width: 30vw;
  }

  &--m {
    width: 40vw;
  }

  &--l {
    width: 55vw;
  }

  &--xl {
    width: 70vw;
  }

  &__close {
    position: absolute;
    top: space(3);
    right: space(3);
  }
}
</style>
