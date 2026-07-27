<template>
    <div class="sa-side-menu" :class="`sa-side-menu--${size}`">
        <h2>{{ title }}</h2>
        <slot />
    </div>

</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string,
    size?: 'xs' | 's' | 'm' | 'l' | 'xl'
  }>(),
  {
    size: 'm',
  },
)

</script>

<style lang="scss">
    @use '@/styles/main' as *;


    .sa-side-menu {
        height: 100vh;
        background-color: $surface-background-secondary;
        padding: space(0) space(4);
        &--xs{
            width: 10vw;
        }
        &--s{
            width: 15vw;
        }
        &--m{
            width: 20vw;
        }
        &--l{
            width: 25vw;
        }
        &--xl{
            width: 30vw;
        }
    }
</style>