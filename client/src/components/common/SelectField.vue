<template>
  <label class="sa-select-field">
    <span class="sa-select-field__label">{{ label }}</span>
    <select
      class="sa-select-field__input"
      :required="required"
      :value="modelValue"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </label>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    required?: boolean
    modelValue: string
    options: { value: string; label: string }[]
  }>(),
  {
    required: false,
  },
)

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-select-field {
  display: flex;
  flex-direction: column;
  gap: space(1);

  &__label {
    font-size: $font-size-s;
  }

  &__input {
    padding: space(2);
    font-family: $font-family-default;
    font-size: $font-size-s;
    color: $font-color-default;
    background-color: $surface-background-default;
    border: 1px solid $surface-border-default;
  }
}
</style>
