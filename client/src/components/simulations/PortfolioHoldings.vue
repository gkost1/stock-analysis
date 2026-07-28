<template>
  <Card class="sa-portfolio-holdings">
    <div class="sa-portfolio-holdings__header">
      <h3>Holdings</h3>
      <div class="sa-portfolio-holdings__header-actions">
        <Button @click="isUploadCsvModalOpen = true">Upload CSV</Button>
        <Button variant="primary" @click="isAddHoldingModalOpen = true">+ Holding</Button>
      </div>
    </div>

    <div class="sa-portfolio-holdings__body">
      <LoadingState v-if="isLoading" message="Loading Holdings" />
      <PortfolioListingTable v-else-if="holdings.length" :holdings="holdings" />
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
import { ref } from 'vue';
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import LoadingState from '@/components/common/LoadingState.vue';
import type { PortfolioHolding } from '@/services/portfolioHoldingsService';
import type { Portfolio } from '@/services/portfolioService';
import AddPortfolioHoldingFormModal from './AddPortfolioHoldingFormModal.vue';
import PortfolioListingTable from './PortfolioListingTable.vue';
import UploadHoldingsCsvModal from './UploadHoldingsCsvModal.vue';

defineProps<{
  portfolio?: Portfolio | null
  holdings: PortfolioHolding[]
  isLoading: boolean
}>();

defineEmits<{
  refresh: []
}>();

const isAddHoldingModalOpen = ref(false);
const isUploadCsvModalOpen = ref(false);
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
