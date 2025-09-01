// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'

const routes = [
  { path: '/dashboard', component: Dashboard },
  // Add other routes here as needed
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
