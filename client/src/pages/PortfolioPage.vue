<template>
  <div class="sa-portfolio-page">
    <SideMenu size="m" title="Existing Portfolios">
      <template #actions>
        <Button variant="primary" @click="isNewPortfolioModalOpen = true">+ New</Button>
      </template>

      <ul class="sa-portfolio-page__portfolio-list">
        <li v-for="p in portfolios" :key="p.id">
          <Button class="sa-portfolio-page__portfolio-list-item" @click="selectPortfolio(p.id)">
            {{ p.title }}
          </Button>
        </li>
      </ul>
    </SideMenu>
    <PortfolioDetail :portfolio="portfolio" />

    <Modal v-model:open="isNewPortfolioModalOpen" width="l">
      <h2>New Portfolio</h2>

      <Form @submit="handleSubmit">
        <FormField v-model="title" label="Portfolio Title" required />
        <FormField v-model="startDate" label="Start Date" type="date" required />
        <FormField v-model="endDate" label="End Date" type="date" required />

        <div class="sa-portfolio-page__form-actions">
          <Button @click="isNewPortfolioModalOpen = false">Cancel</Button>
          <Button type="submit" variant="primary">Create Portfolio</Button>
        </div>
      </Form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Button from '@/components/common/Button.vue';
import Form from '@/components/common/Form.vue';
import FormField from '@/components/common/FormField.vue';
import Modal from '@/components/common/Modal.vue';
import SideMenu from '@/components/common/SideMenu.vue';
import PortfolioDetail from '@/components/simulations/PortfolioDetail.vue';
import { portfolioService, type Portfolio } from '@/services/portfolioService';

const route = useRoute();
const router = useRouter();

const isNewPortfolioModalOpen = ref(false);
const title = ref('');
const startDate = ref('');
const endDate = ref('');
const portfolio = ref<Portfolio | null>(null);
const portfolios = ref<Portfolio[]>([]);

async function loadPortfolios() {
  portfolios.value = await portfolioService.list();
}

function selectPortfolio(id: number) {
  router.push(`/portfolios/${id}`);
}

async function handleSubmit() {
  const created = await portfolioService.create({
    title: title.value,
    start_date: startDate.value,
    end_date: endDate.value,
  });
  portfolio.value = await portfolioService.retrieve(created.id);
  await loadPortfolios();

  isNewPortfolioModalOpen.value = false;
  title.value = '';
  startDate.value = '';
  endDate.value = '';
}

async function loadSelectedPortfolio(id: string | string[] | undefined) {
  portfolio.value = id ? await portfolioService.retrieve(Number(id)) : null;
}

watch(() => route.params.id, loadSelectedPortfolio, { immediate: true });

onMounted(loadPortfolios);
</script>

<style lang="scss">
  @use '@/styles/main' as *;
  .sa-portfolio-page {
    display: flex;

    &__portfolio-list {
      display: flex;
      flex-direction: column;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .sa-button.sa-portfolio-page__portfolio-list-item {
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
