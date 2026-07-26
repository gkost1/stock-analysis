import { createRouter, createWebHistory } from 'vue-router'
import Simulations from '../pages/Simulations.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/simulations',
      name: 'simulations',
      component: Simulations,
    },
  ],
})

export default router
