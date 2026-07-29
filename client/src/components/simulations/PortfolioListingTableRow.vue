<template>
  <tr class="sa-portfolio-listing-row">
    <td>{{ rowNumber }}</td>
    <td>{{ holding.ticker }}</td>
    <td>{{ formatShares(holding.quantity) }}</td>
    <td>{{ formatCurrency(holding.cost_per_share) }}</td>
    <td>{{ holding.date_purchased }}</td>
    <td>{{ formatCurrency(holding.current_share_price) }}</td>
    <td>{{ formatCurrency(holding.total_cost) }}</td>
    <td>{{ formatCurrency(holding.total_value) }}</td>
    <td
      :class="{
        'sa-portfolio-listing-row--profit': profitLoss !== null && profitLoss >= 0,
        'sa-portfolio-listing-row--loss': profitLoss !== null && profitLoss < 0,
      }"
    >
      {{ formatCurrency(holding.profit_loss) }}
    </td>
  </tr>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PortfolioHolding } from '@/services/portfolioHoldingsService';

const props = defineProps<{
  rowNumber: number
  holding: PortfolioHolding
}>();

function formatCurrency(value: string | null) {
  if (value === null) return '—';
  return `$${Number(value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatShares(value: string) {
  return Number(value).toLocaleString(undefined, { maximumFractionDigits: 6 });
}

const profitLoss = computed(() => {
  const value = props.holding.profit_loss;
  return value === null ? null : Number(value);
});
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-portfolio-listing-row {
  &--profit {
    color: $font-color-positive;
  }

  &--loss {
    color: $font-color-negative;
  }
}
</style>
