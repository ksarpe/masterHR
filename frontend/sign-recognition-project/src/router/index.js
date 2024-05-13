import { createRouter, createWebHashHistory } from 'vue-router'

import IndexView from '@/views/IndexView.vue'
import PathView  from '@/views/PathView.vue'
import IntroductionFirstView from '@/views/IntroductionFirstView.vue'

const routes = [
  { path: '/', name: 'Home', component: IndexView },
  { path: '/learn', name: 'Learn', component: PathView },
  { path: '/learn/introduction', name: 'IntroductionFirst', component: IntroductionFirstView },
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
