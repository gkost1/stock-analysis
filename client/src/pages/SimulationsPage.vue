<template>
  <div class="sa-simulations-page">
    <SideMenu size="m" title="Existing Studies">
      <template #actions>
        <Button variant="primary" @click="isNewStudyModalOpen = true">+ New</Button>
      </template>

      <ul class="sa-simulations-page__study-list">
        <li v-for="s in studies" :key="s.id">
          <Button class="sa-simulations-page__study-list-item" @click="selectStudy(s.id)">
            {{ s.title }}
          </Button>
        </li>
      </ul>
    </SideMenu>
    <SimulationDetails />

    <Modal v-model:open="isNewStudyModalOpen" width="l">
      <h2>New Study</h2>

      <Form @submit="handleSubmit">
        <FormField v-model="title" label="Study Title" required />
        <FormField v-model="startDate" label="Start Date" type="date" required />
        <FormField v-model="endDate" label="End Date" type="date" required />

        <div class="sa-simulations-page__form-actions">
          <Button @click="isNewStudyModalOpen = false">Cancel</Button>
          <Button type="submit" variant="primary">Create Study</Button>
        </div>
      </Form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import Button from '@/components/common/Button.vue';
import Form from '@/components/common/Form.vue';
import FormField from '@/components/common/FormField.vue';
import Modal from '@/components/common/Modal.vue';
import SideMenu from '@/components/common/SideMenu.vue';
import SimulationDetails from '@/components/simulations/SimulationDetails.vue';
import { studyService, type Study } from '@/services/studyService';

const router = useRouter();

const isNewStudyModalOpen = ref(false);
const title = ref('');
const startDate = ref('');
const endDate = ref('');
const study = ref<Study | null>(null);
const studies = ref<Study[]>([]);

async function loadStudies() {
  studies.value = await studyService.list();
}

function selectStudy(id: number) {
  router.push(`/simulations/${id}`);
}

async function handleSubmit() {
  const created = await studyService.create({
    title: title.value,
    start_date: startDate.value,
    end_date: endDate.value,
  });
  study.value = await studyService.retrieve(created.id);
  await loadStudies();

  isNewStudyModalOpen.value = false;
  title.value = '';
  startDate.value = '';
  endDate.value = '';
}

onMounted(loadStudies);
</script>

<style lang="scss">
  @use '@/styles/main' as *;
  .sa-simulations-page {
    display: flex;

    &__study-list {
      display: flex;
      flex-direction: column;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .sa-button.sa-simulations-page__study-list-item {
      justify-content: flex-start;
      width: 100%;
      padding: space(2) space(4);
      text-align: left;

      &:hover {
        background-color: $surface-background-secondary-hover;
      }
    }

    &__form-actions {
      display: flex;
      justify-content: flex-end;
      gap: space(2);
    }
  }
</style>
