<script setup lang="ts">
withDefaults(
  defineProps<{
    name: string
    size?: 'xs' | 's' | 'm' | 'l' | 'xl'
  }>(),
  {
    size: 'm',
  },
)
</script>

<template>
  <svg class="sa-icon" :class="`sa-icon--${size}`" aria-hidden="true">
    <use :href="`#icon-${name}`" />
  </svg>
</template>

<style scoped lang="scss">
@use '@/styles/colors';
@use '@/styles/typography';

.sa-icon {
  color: colors.$icon-color-default;
  fill: currentColor;

  &--xs {
    width: typography.$icon-size-xs;
    height: typography.$icon-size-xs;
  }

  &--s {
    width: typography.$icon-size-s;
    height: typography.$icon-size-s;
  }

  &--m {
    width: typography.$icon-size-m;
    height: typography.$icon-size-m;
  }

  &--l {
    width: typography.$icon-size-l;
    height: typography.$icon-size-l;
  }

  &--xl {
    width: typography.$icon-size-xl;
    height: typography.$icon-size-xl;
  }
}
</style>
