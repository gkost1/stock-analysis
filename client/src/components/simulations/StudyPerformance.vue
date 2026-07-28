<template>
  <Card class="sa-study-performance">
    <div class="sa-study-performance__header">
      <h3>Performance</h3>
      <Button variant="primary" @click="isAddViewModalOpen = true">+ View</Button>
    </div>

    <EmptyState v-if="!views.length" message="No views yet." />
    <div v-else class="sa-study-performance__grid">
      <PerformanceChartTile
        v-for="view in views"
        :key="view.id"
        :view="view"
        @remove="removeView(view)"
      />
    </div>

    <AddPerformanceViewModal
      v-model:open="isAddViewModalOpen"
      :study="study"
      :tickers="tickers"
      @created="loadViews"
    />
  </Card>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import { portfolioHoldingsService } from '@/services/portfolioHoldingsService';
import { studyService, type Study } from '@/services/studyService';
import { studyViewsService, type StudyView } from '@/services/studyViewsService';
import AddPerformanceViewModal from './AddPerformanceViewModal.vue';
import PerformanceChartTile from './PerformanceChartTile.vue';

const props = defineProps<{
  study?: Study | null
}>();

const isAddViewModalOpen = ref(false);
const tickers = ref<string[]>([]);
const views = ref<StudyView[]>([]);

async function loadTickers() {
  if (!props.study) {
    tickers.value = [];
    return;
  }

  const holdings = await portfolioHoldingsService.list(props.study.id);
  tickers.value = [...new Set(holdings.map((holding) => holding.ticker))];
}

async function loadViews() {
  if (!props.study) {
    views.value = [];
    return;
  }

  const updated = await studyService.retrieve(props.study.id);
  views.value = updated.views;
}

async function removeView(view: StudyView) {
  if (!props.study) return;

  await studyViewsService.delete(view.id);
  await loadViews();
}

watch(() => props.study, loadTickers, { immediate: true });
watch(() => props.study, loadViews, { immediate: true });

onMounted(() => {
  loadTickers();
  loadViews();
});
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-study-performance {
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
