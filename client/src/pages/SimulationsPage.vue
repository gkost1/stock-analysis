<template>
  <div class="sa-simulations-page">
    <SideMenu size="m" title="Existing Studies">

    </SideMenu>
    <SimulationDetails />
    
  </div>
</template>

<script setup lang="ts">
import SideMenu from '@/components/common/SideMenu.vue';
import SimulationDetails from '@/components/simulations/SimulationDetails.vue';
</script>

<style >
  .sa-simulations-page {
    display: flex;

  }
</style>
