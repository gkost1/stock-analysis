<template>
  <Card class="sa-portfolio-holdings">
    <h3>Holdings</h3>
    <div class="sa-portfolio-holdings__body">
      <Button variant="primary">+ Holding</Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-portfolio-holdings {
  display: flex;
  flex-direction: column;

  &__body {
    display: flex;
    flex: 1;
    align-items: center;
    justify-content: center;
  }
}
</style>
