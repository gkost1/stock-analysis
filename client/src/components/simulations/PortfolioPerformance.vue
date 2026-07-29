<template>
  <Card class="sa-portfolio-performance">
    <div class="sa-portfolio-performance__header">
      <h3>Performance</h3>
      <Button variant="primary" @click="isAddViewModalOpen = true">+ View</Button>
    </div>

    <EmptyState v-if="!views.length" message="No views yet." />
    <div v-else class="sa-portfolio-performance__grid">
      <PerformanceChartTile
        v-for="view in views"
        :key="view.id"
        :view="view"
        @remove="removeView(view)"
      />
    </div>

    <AddPerformanceViewModal
      v-model:open="isAddViewModalOpen"
      :portfolio="portfolio"
      :tickers="tickers"
      @created="loadViews"
    />
  </Card>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import type { PortfolioHolding } from '@/services/portfolioHoldingsService';
import { portfolioService, type Portfolio } from '@/services/portfolioService';
import { portfolioViewsService, type PortfolioView } from '@/services/portfolioViewsService';
import AddPerformanceViewModal from './AddPerformanceViewModal.vue';
import PerformanceChartTile from './PerformanceChartTile.vue';

const props = defineProps<{
  portfolio?: Portfolio | null
  holdings: PortfolioHolding[]
}>();

const isAddViewModalOpen = ref(false);
const views = ref<PortfolioView[]>([]);

const tickers = computed(() => [...new Set(props.holdings.map((holding) => holding.ticker))]);

async function loadViews() {
  if (!props.portfolio) {
    views.value = [];
    return;
  }

  const updated = await portfolioService.retrieve(props.portfolio.id);
  views.value = updated.views;
}

async function removeView(view: PortfolioView) {
  if (!props.portfolio) return;

  await portfolioViewsService.delete(view.id);
  await loadViews();
}

watch(() => props.portfolio, (portfolio) => {
  views.value = portfolio?.views ?? [];
}, { immediate: true });
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-portfolio-performance {
  // Combined with .sa-card for specificity, to override Card's fixed height —
  // this card grows with its tiles and the page scrolls, not the card.
  &.sa-card {
    height: auto;
  }

  display: flex;
  flex-direction: column;
  gap: space(2);

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    h3 {
      margin: 0;
    }
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: space(4);
  }
}
</style>
