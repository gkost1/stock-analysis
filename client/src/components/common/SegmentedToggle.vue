<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  modelValue: string
  options: { label: string; value: string }[]
}>();

defineEmits<{
  'update:modelValue': [value: string]
}>();

const activeIndex = computed(() => props.options.findIndex((option) => option.value === props.modelValue));
</script>

<template>
  <div class="sa-segmented-toggle" :style="{ '--count': options.length }">
    <div class="sa-segmented-toggle__thumb" :style="{ transform: `translateX(${activeIndex * 100}%)` }" />
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      class="sa-segmented-toggle__option"
      :class="{ 'sa-segmented-toggle__option--active': option.value === modelValue }"
      @click="$emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-segmented-toggle {
  position: relative;
  display: grid;
  grid-template-columns: repeat(var(--count), 1fr);
  padding: 3px;
  background: $button-background-primary;
  border-radius: 999px;

  &__thumb {
    position: absolute;
    top: 3px;
    bottom: 3px;
    left: 3px;
    width: calc((100% - 6px) / var(--count));
    background: $gray-100;
    border-radius: 999px;
    transition: transform 0.2s ease;
  }

  &__option {
    position: relative;
    z-index: 1;
    padding: space(1) space(3);
    font-family: $font-family-default;
    font-size: $font-size-s;
    font-weight: 600;
    color: $gray-100;
    white-space: nowrap;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.2s ease;

    &--active {
      color: $button-background-primary;
    }
  }
}
</style>
