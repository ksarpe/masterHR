import { createRouter, createWebHashHistory } from 'vue-router'

import IndexView from '@/views/IndexView.vue'
import PathView  from '@/views/PathView.vue'
import TestsPathView from '@/views/TestsPathView.vue'
import GamesPathView from '@/views/GamesPathView.vue'
import CommunityView from '@/views/CommunityView.vue'
import HelpView from '@/views/HelpView.vue'
import IntroductionFirstView from '@/views/IntroductionFirstView.vue'
import IntroductionTestView from '@/views/IntroductionTestView.vue'
import IntroductionGameView from '@/views/IntroductionGameView.vue'

const routes = [
  { path: '/', name: 'Home', component: IndexView },
  { path: '/learn', name: 'Learn', component: PathView },
  { path: '/tests', name: 'Tests', component: TestsPathView },
  { path: '/games', name: 'Games', component: GamesPathView },
  { path: '/community', name: 'Community', component: CommunityView },
  { path: '/help', name: 'Help', component: HelpView },
  { path: '/learn/introduction', name: 'IntroductionFirst', component: IntroductionFirstView },
  { path: '/tests/test-introduction', name: 'IntroductionTest', component: IntroductionTestView },
  { path: '/games/game-introduction', name: 'IntroductionGame', component: IntroductionGameView },
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
