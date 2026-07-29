<template>
    <div class="sa-top-bar">
        <h1>Stock Analyzer</h1>
        <div class="sa-top-bar__menu">
            <Button class="sa-top-bar__menu-button" @click.stop="isMenuOpen = !isMenuOpen">
                <Icon name="hamburger_menu" size="xl" />
            </Button>
            <DropdownMenu v-model:open="isMenuOpen">
                <DropdownItem @click="onSimulationsClick">Simulations</DropdownItem>
                <DropdownItem @click="onLogoutClick">Log out</DropdownItem>
            </DropdownMenu>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Icon from './Icon.vue'
import Button from './Button.vue'
import DropdownMenu from './DropdownMenu.vue'
import DropdownItem from './DropdownItem.vue'

const emit = defineEmits<{
    logout: []
}>()

const router = useRouter()
const isMenuOpen = ref(false)

function onSimulationsClick() {
    isMenuOpen.value = false
    router.push({ name: 'simulations' })
}

function onLogoutClick() {
    isMenuOpen.value = false
    emit('logout')
}
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

    &__menu {
        position: relative;
        display: flex;
    }

    &__menu-button {
        &:hover .sa-icon {
            color: $icon-color-hover;
        }
    }
}
</style>