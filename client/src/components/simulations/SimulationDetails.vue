<template>
    <div class="sa-simulation-detail">
      <h2>{{ study?.title }}</h2>
      <StudyPerformance />
      <PortfolioHoldings />
    </div>
  </template>

  <script setup lang="ts">
  import type { Study } from '@/services/studyService';
  import PortfolioHoldings from './PortfolioHoldings.vue';
  import StudyPerformance from './StudyPerformance.vue';

  defineProps<{
    study?: Study | null
  }>();
  </script>

  <style lang="scss">
    @use '@/styles/main' as *;
    .sa-simulation-detail {
      display: flex;
      flex: 1;
      flex-direction: column;
      gap: space(4);
      padding: 0 space(4);
    }
  </style>
