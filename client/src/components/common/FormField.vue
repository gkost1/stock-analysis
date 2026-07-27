<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    type?: string
    required?: boolean
    modelValue: string
  }>(),
  {
    type: 'text',
    required: false,
  },
)

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <label class="sa-form-field">
    <span class="sa-form-field__label">{{ label }}</span>
    <input
      class="sa-form-field__input"
      :type="type"
      :required="required"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </label>
</template>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-form-field {
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
