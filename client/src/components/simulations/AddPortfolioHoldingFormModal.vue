<template>
  <Modal v-model:open="open" width="s">
    <h2>New Holding</h2>

    <Form @submit="handleSubmit">
      <FormField v-model="ticker" label="Ticker" required />
      <FormField v-model="quantity" label="Shares" type="number" required />
      <FormField v-model="costPerShare" label="Cost per Share" type="number" required />
      <FormField v-model="datePurchased" label="Date Purchased" type="date" required />
      <FormField v-model="dateSold" label="Date Sold" type="date" />

      <div class="sa-add-portfolio-holding-form-modal__actions">
        <Button @click="open = false">Cancel</Button>
        <Button type="submit" variant="primary">Add Holding</Button>
      </div>
    </Form>
  </Modal>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Button from '@/components/common/Button.vue';
import Form from '@/components/common/Form.vue';
import FormField from '@/components/common/FormField.vue';
import Modal from '@/components/common/Modal.vue';
import { portfolioHoldingsService } from '@/services/portfolioHoldingsService';
import type { Study } from '@/services/studyService';

const props = defineProps<{
  study?: Study | null
}>();

const emit = defineEmits<{
  created: []
}>();

const open = defineModel<boolean>('open', { default: false });

const ticker = ref('');
const quantity = ref('');
const costPerShare = ref('');
const datePurchased = ref('');
const dateSold = ref('');

async function handleSubmit() {
  if (!props.study) return;

  await portfolioHoldingsService.create(props.study.id, {
    ticker: ticker.value,
    quantity: quantity.value,
    cost_per_share: costPerShare.value,
    date_purchased: datePurchased.value,
    date_sold: dateSold.value || null,
  });

  open.value = false;
  ticker.value = '';
  quantity.value = '';
  costPerShare.value = '';
  datePurchased.value = '';
  dateSold.value = '';

  emit('created');
}
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-add-portfolio-holding-form-modal {
  &__actions {
    display: flex;
    justify-content: flex-end;
    gap: space(2);
  }
}
</style>
