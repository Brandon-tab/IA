import { createRouter, createWebHistory } from 'vue-router'
import TablePage from '../views/TablePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'TablePage',
      component: TablePage
    }
  ],
})

export default router
