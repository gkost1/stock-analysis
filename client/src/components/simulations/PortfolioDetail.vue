<template>
    <div class="sa-portfolio-detail">
      <h2>{{ portfolio?.title }}</h2>
      <PortfolioPerformance :portfolio="portfolio" :holdings="holdings" />
      <PortfolioHoldings :portfolio="portfolio" :holdings="holdings" :is-loading="isLoadingHoldings" @refresh="loadHoldings" />
    </div>
  </template>

  <script setup lang="ts">
  import { ref, watch } from 'vue';
  import { portfolioHoldingsService, type PortfolioHolding } from '@/services/portfolioHoldingsService';
  import type { Portfolio } from '@/services/portfolioService';
  import PortfolioHoldings from './PortfolioHoldings.vue';
  import PortfolioPerformance from './PortfolioPerformance.vue';

  const props = defineProps<{
    portfolio?: Portfolio | null
  }>();

  const holdings = ref<PortfolioHolding[]>([]);
  const isLoadingHoldings = ref(false);

  async function loadHoldings() {
    if (!props.portfolio) {
      holdings.value = [];
      return;
    }

    isLoadingHoldings.value = true;
    try {
      holdings.value = await portfolioHoldingsService.list(props.portfolio.id);
    } finally {
      isLoadingHoldings.value = false;
    }
  }

  watch(() => props.portfolio, loadHoldings, { immediate: true });
  </script>

  <style lang="scss">
    @use '@/styles/main' as *;
    .sa-portfolio-detail {
      display: flex;
      flex: 1;
      flex-direction: column;
      gap: space(4);
      padding: 0 space(4);
    }
  </style>
