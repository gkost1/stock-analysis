import { createRouter, createWebHistory } from 'vue-router'
import SimulationsPage from '../pages/SimulationsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/simulations',
      name: 'simulations',
      component: SimulationsPage,
    },
  ],
})

export default router
