<template>
  <Modal v-model:open="open" width="s">
    <h2>Add View</h2>

    <Form @submit="handleSubmit">
      <SelectField v-model="asset" label="Asset" :options="assetOptions" required />
      <SelectField v-model="xAxis" label="X-Axis" :options="xAxisOptions" required />
      <SelectField v-model="yAxis" label="Y-Axis" :options="yAxisOptions" required />

      <div class="sa-add-performance-view-modal__actions">
        <Button @click="open = false">Cancel</Button>
        <Button type="submit" variant="primary">Add View</Button>
      </div>
    </Form>
  </Modal>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import Button from '@/components/common/Button.vue';
import Form from '@/components/common/Form.vue';
import Modal from '@/components/common/Modal.vue';
import SelectField from '@/components/common/SelectField.vue';
import { portfolioViewsService, type PortfolioViewYAxis } from '@/services/portfolioViewsService';
import type { Portfolio } from '@/services/portfolioService';

const PORTFOLIO_ASSET = '__portfolio__';

const props = defineProps<{
  portfolio?: Portfolio | null
  tickers: string[]
}>();

const emit = defineEmits<{
  created: []
}>();

const open = defineModel<boolean>('open', { default: false });

const asset = ref(PORTFOLIO_ASSET);
const xAxis = ref('time');
const yAxis = ref<PortfolioViewYAxis>('value');

const assetOptions = computed(() => [
  { value: PORTFOLIO_ASSET, label: 'Complete Portfolio' },
  ...props.tickers.map((ticker) => ({ value: ticker, label: ticker })),
]);

const xAxisOptions = [{ value: 'time', label: 'Time' }];

const yAxisOptions = [
  { value: 'value', label: 'Value' },
  { value: 'profit_loss', label: 'Profit/Loss' },
  { value: 'cagr', label: 'CAGR' },
];

async function handleSubmit() {
  if (!props.portfolio) return;

  await portfolioViewsService.create({
    portfolio: props.portfolio.id,
    asset: asset.value === PORTFOLIO_ASSET ? null : asset.value,
    x_axis: xAxis.value,
    y_axis: yAxis.value,
  });

  open.value = false;
  asset.value = PORTFOLIO_ASSET;
  yAxis.value = 'value';

  emit('created');
}
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-add-performance-view-modal {
  &__actions {
    display: flex;
    justify-content: flex-end;
    gap: space(2);
  }
}
</style>
