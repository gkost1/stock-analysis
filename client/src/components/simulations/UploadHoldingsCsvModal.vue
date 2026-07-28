<template>
  <Modal v-model:open="open" width="s">
    <h2>Upload Holdings CSV</h2>

    <Form @submit="handleSubmit">
      <SelectField v-model="source" label="Source" :options="sourceOptions" required />

      <label class="sa-upload-holdings-csv-modal__file-field">
        <span class="sa-upload-holdings-csv-modal__file-label">File</span>
        <input type="file" accept=".csv" required @change="handleFileChange" />
      </label>

      <p v-if="error" class="sa-upload-holdings-csv-modal__error">{{ error }}</p>

      <div class="sa-upload-holdings-csv-modal__actions">
        <Button @click="open = false">Cancel</Button>
        <Button type="submit" variant="primary" :disabled="!file || isUploading">Upload</Button>
      </div>
    </Form>
  </Modal>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Button from '@/components/common/Button.vue';
import Form from '@/components/common/Form.vue';
import Modal from '@/components/common/Modal.vue';
import SelectField from '@/components/common/SelectField.vue';
import { portfolioHoldingsService } from '@/services/portfolioHoldingsService';
import type { Study } from '@/services/studyService';

const props = defineProps<{
  study?: Study | null
}>();

const emit = defineEmits<{
  uploaded: []
}>();

const open = defineModel<boolean>('open', { default: false });

const source = ref('chase_brokerage');
const file = ref<File | null>(null);
const error = ref('');
const isUploading = ref(false);

const sourceOptions = [{ value: 'chase_brokerage', label: 'Chase Brokerage CSV' }];

function handleFileChange(event: Event) {
  file.value = (event.target as HTMLInputElement).files?.[0] ?? null;
}

async function handleSubmit() {
  if (!props.study || !file.value) return;

  error.value = '';
  isUploading.value = true;
  try {
    await portfolioHoldingsService.uploadCsv(props.study.id, source.value, file.value);
    open.value = false;
    file.value = null;
    emit('uploaded');
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
  } finally {
    isUploading.value = false;
  }
}
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-upload-holdings-csv-modal {
  &__file-field {
    display: flex;
    flex-direction: column;
    gap: space(1);
  }

  &__file-label {
    font-size: $font-size-s;
  }

  &__error {
    color: $font-color-negative;
  }

  &__actions {
    display: flex;
    justify-content: flex-end;
    gap: space(2);
  }
}
</style>
