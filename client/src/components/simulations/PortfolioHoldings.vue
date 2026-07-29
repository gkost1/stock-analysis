<template>
  <Card class="sa-portfolio-holdings">
    <div class="sa-portfolio-holdings__header">
      <h3>Holdings</h3>
      <div class="sa-portfolio-holdings__header-actions">
        <SegmentedToggle
          v-model="viewMode"
          :options="[
            { label: 'By Ticker', value: 'consolidated' },
            { label: 'By Lot', value: 'detailed' },
          ]"
        />
        <Button @click="isUploadCsvModalOpen = true">Upload CSV</Button>
        <Button variant="primary" @click="isAddHoldingModalOpen = true">+ Holding</Button>
      </div>
    </div>

    <div class="sa-portfolio-holdings__body">
      <LoadingState v-if="isDisplayLoading" message="Loading Holdings" />
      <PortfolioListingTable v-else-if="displayedHoldings.length" :holdings="displayedHoldings" />
      <EmptyState v-else message="No holdings yet." />
    </div>

    <AddPortfolioHoldingFormModal
      v-model:open="isAddHoldingModalOpen"
      :portfolio="portfolio"
      @created="$emit('refresh')"
    />

    <UploadHoldingsCsvModal
      v-model:open="isUploadCsvModalOpen"
      :portfolio="portfolio"
      @uploaded="$emit('refresh')"
    />
  </Card>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import LoadingState from '@/components/common/LoadingState.vue';
import SegmentedToggle from '@/components/common/SegmentedToggle.vue';
import { portfolioHoldingsService, type PortfolioHolding } from '@/services/portfolioHoldingsService';
import type { Portfolio } from '@/services/portfolioService';
import AddPortfolioHoldingFormModal from './AddPortfolioHoldingFormModal.vue';
import PortfolioListingTable from './PortfolioListingTable.vue';
import UploadHoldingsCsvModal from './UploadHoldingsCsvModal.vue';

const props = defineProps<{
  portfolio?: Portfolio | null
  holdings: PortfolioHolding[]
  isLoading: boolean
}>();

defineEmits<{
  refresh: []
}>();

const isAddHoldingModalOpen = ref(false);
const isUploadCsvModalOpen = ref(false);
const viewMode = ref<'consolidated' | 'detailed'>('consolidated');

const consolidatedHoldings = ref<PortfolioHolding[]>([]);
const isLoadingConsolidated = ref(false);

async function loadConsolidatedHoldings() {
  if (!props.portfolio) {
    consolidatedHoldings.value = [];
    return;
  }

  isLoadingConsolidated.value = true;
  try {
    consolidatedHoldings.value = await portfolioHoldingsService.list(props.portfolio.id, { consolidate: true });
  } finally {
    isLoadingConsolidated.value = false;
  }
}

watch([() => props.portfolio, () => props.holdings], loadConsolidatedHoldings, { immediate: true });

const displayedHoldings = computed(() =>
  viewMode.value === 'consolidated' ? consolidatedHoldings.value : props.holdings,
);

const isDisplayLoading = computed(
  () => props.isLoading || (viewMode.value === 'consolidated' && isLoadingConsolidated.value),
);
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-portfolio-holdings {
  // Combined with .sa-card for specificity, to override Card's fixed height.
  &.sa-card {
    height: auto;
    max-height: 50vh;
  }

  display: flex;
  flex-direction: column;
  gap: space(2);

  &__header {
    display: flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: space-between;

    h3 {
      margin: 0;
    }
  }

  &__header-actions {
    display: flex;
    align-items: center;
    gap: space(2);
  }

  &__body {
    display: flex;
    flex: 1;
    min-height: 0;
    overflow-y: auto;
  }
}
</style>
