<template>
  <Card class="sa-study-performance">
    <h3>Performance</h3>
    <div class="sa-study-performance__body">
      <Button variant="primary">+ View</Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-study-performance {
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
