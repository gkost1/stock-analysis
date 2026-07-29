<template>
  <table class="sa-portfolio-listing-table">
    <colgroup>
      <col style="width: 8%" />
      <col style="width: 10%" />
      <col style="width: 8%" />
      <col style="width: 12%" />
      <col style="width: 13%" />
      <col style="width: 12%" />
      <col style="width: 12%" />
      <col style="width: 12%" />
      <col style="width: 13%" />
    </colgroup>
    <thead>
      <tr>
        <th>Row #</th>
        <th>Ticker</th>
        <th>Shares</th>
        <th>Cost per Share</th>
        <th>Date Purchased</th>
        <th>Current Price</th>
        <th>Total Cost</th>
        <th>Total Value</th>
        <th>Profit (Loss)</th>
      </tr>
    </thead>
    <tbody>
      <PortfolioListingTableRow
        v-for="(holding, index) in holdings"
        :key="holding.id"
        :row-number="index + 1"
        :holding="holding"
      />
    </tbody>
  </table>
</template>

<script setup lang="ts">
import type { PortfolioHolding } from '@/services/portfolioHoldingsService';
import PortfolioListingTableRow from './PortfolioListingTableRow.vue';

defineProps<{
  holdings: PortfolioHolding[]
}>();
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-portfolio-listing-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  font-size: $font-size-s;

  th,
  :deep(td) {
    padding: space(1) space(2);
    overflow: hidden;
    text-align: left;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  th {
    border-bottom: 1px solid $surface-border-default;
  }
}
</style>
