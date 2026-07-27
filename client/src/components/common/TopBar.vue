<template>
    <div class="sa-top-bar">
        <h1>Stock Analyzer</h1>
        <Button class="sa-top-bar__menu-button">
            <Icon name="hamburger_menu" size="xl" />
        </Button>
    </div>
</template>

<script setup lang="ts">
import Icon from './Icon.vue'
import Button from './Button.vue'
</script>


<style lang="scss">
@use '@/styles/main' as *;

.sa-top-bar {
    padding: space(4) space(4) space(1) space(4);
    background-color: $surface-background-default;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid $surface-border-default;

    &__menu-button {
        &:hover .sa-icon {
            color: $icon-color-hover;
        }
    }
}
</style>