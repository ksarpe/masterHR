import { createRouter, createWebHashHistory } from 'vue-router'

import IndexView from '../views/IndexView.vue'

const routes = [
  { path: '/', name: 'Home', component: IndexView },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return {
      top: 0,
      left: 0,
      behavior: 'smooth'
    }
  }
})

export default router
