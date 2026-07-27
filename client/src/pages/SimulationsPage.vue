<template>
  <div class="sa-simulations-page">
    <SideMenu size="m" title="Existing Studies">
      <template #actions>
        <Button class="sa-simulations-page__new-button" @click="isNewStudyModalOpen = true">+ New</Button>
      </template>
    </SideMenu>
    <SimulationDetails />

    <Modal v-model:open="isNewStudyModalOpen" width="l">
      <h2>New Study</h2>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Button from '@/components/common/Button.vue';
import Modal from '@/components/common/Modal.vue';
import SideMenu from '@/components/common/SideMenu.vue';
import SimulationDetails from '@/components/simulations/SimulationDetails.vue';

const isNewStudyModalOpen = ref(false);
</script>

<style lang="scss">
  @use '@/styles/main' as *;
  .sa-simulations-page {
    display: flex;

    .sa-button.sa-simulations-page__new-button {
      border: 1px solid $button-border-primary;
      border-radius: 4px;
      padding: space(1) space(2);
      background: $button-background-primary;

      &:hover{
        background: $button-background-primary-hover;
      }
    }

  }
</style>
