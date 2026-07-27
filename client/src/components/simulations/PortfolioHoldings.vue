<template>
  <Card class="sa-portfolio-holdings">
    <div class="sa-portfolio-holdings__header">
      <h3>Holdings</h3>
      <Button variant="primary" @click="isAddHoldingModalOpen = true">+ Holding</Button>
    </div>

    <div class="sa-portfolio-holdings__body">
      <LoadingState v-if="isLoading" message="Loading Holdings" />
      <PortfolioListingTable v-else-if="holdings.length" :holdings="holdings" />
      <EmptyState v-else message="No holdings yet." />
    </div>

    <AddPortfolioHoldingFormModal
      v-model:open="isAddHoldingModalOpen"
      :study="study"
      @created="loadHoldings"
    />
  </Card>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import Button from '@/components/common/Button.vue';
import Card from '@/components/common/Card.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import LoadingState from '@/components/common/LoadingState.vue';
import { portfolioHoldingsService, type PortfolioHolding } from '@/services/portfolioHoldingsService';
import type { Study } from '@/services/studyService';
import AddPortfolioHoldingFormModal from './AddPortfolioHoldingFormModal.vue';
import PortfolioListingTable from './PortfolioListingTable.vue';

const props = defineProps<{
  study?: Study | null
}>();

const isAddHoldingModalOpen = ref(false);
const isLoading = ref(false);
const holdings = ref<PortfolioHolding[]>([]);

async function loadHoldings() {
  if (!props.study) {
    holdings.value = [];
    return;
  }

  isLoading.value = true;
  try {
    holdings.value = await portfolioHoldingsService.list(props.study.id);
  } finally {
    isLoading.value = false;
  }
}

watch(() => props.study, loadHoldings, { immediate: true });

onMounted(loadHoldings);
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

  &__body {
    display: flex;
    flex: 1;
    min-height: 0;
    overflow-y: auto;
  }
}
</style>
