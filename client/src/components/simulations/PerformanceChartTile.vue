<template>
  <div class="sa-performance-chart-tile">
    <div class="sa-performance-chart-tile__header">
      <span class="sa-performance-chart-tile__title">{{ title }}</span>
      <Button @click="$emit('remove')">
        <Icon name="close" size="s" />
      </Button>
    </div>

    <div class="sa-performance-chart-tile__body">
      <LoadingState v-if="isLoading" message="Loading" />
      <EmptyState v-else-if="!points.length" message="No performance data yet." />
      <Line v-else :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js';
import { computed, onMounted, ref, watch } from 'vue';
import { Line } from 'vue-chartjs';
import Button from '@/components/common/Button.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import Icon from '@/components/common/Icon.vue';
import LoadingState from '@/components/common/LoadingState.vue';
import { portfolioViewsService, type PerformancePoint, type PortfolioView } from '@/services/portfolioViewsService';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, LineController, Tooltip, Legend);

const props = defineProps<{
  view: PortfolioView
}>();

defineEmits<{
  remove: []
}>();

const isLoading = ref(false);
const points = ref<PerformancePoint[]>([]);

const Y_AXIS_LABELS: Record<PortfolioView['y_axis'], string> = {
  value: 'Value',
  profit_loss: 'Profit/Loss',
  cagr: 'CAGR',
};

const title = computed(() => {
  const asset = props.view.asset ?? 'Complete Portfolio';
  return `${asset} — ${Y_AXIS_LABELS[props.view.y_axis]}`;
});

const chartData = computed(() => ({
  labels: points.value.map((point) => point.date),
  datasets: [
    {
      label: Y_AXIS_LABELS[props.view.y_axis],
      data: points.value.map((point) => {
        const raw = point[props.view.y_axis];
        return raw !== null ? Number(raw) : null;
      }),
      borderColor: '#7e22ce',
      backgroundColor: '#7e22ce',
      spanGaps: true,
      pointRadius: 0,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
};

async function loadPerformance() {
  isLoading.value = true;
  try {
    points.value = await portfolioViewsService.performance(props.view.id);
  } finally {
    isLoading.value = false;
  }
}

watch(() => props.view, loadPerformance, { deep: true });

onMounted(loadPerformance);
</script>

<style scoped lang="scss">
@use '@/styles/main' as *;

.sa-performance-chart-tile {
  display: flex;
  flex-direction: column;
  gap: space(2);
  padding: space(2);
  background-color: $surface-background-default;
  border: 1px solid $surface-border-default;
  border-radius: 4px;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__title {
    font-size: $font-size-s;
  }

  &__body {
    position: relative;
    height: 240px;
  }
}
</style>
