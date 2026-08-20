import { createRouter, createWebHistory } from 'vue-router'

/**
 * 路由配置
 * /        → 首页（星梦智能助手入口）
 * /star    → 星座星盘分析测算页
 * /dream   → 周公解梦页
 */
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/star',
    name: 'StarAnalysis',
    component: () => import('@/views/StarAnalysis.vue'),
  },
  {
    path: '/dream',
    name: 'DreamInterpretation',
    component: () => import('@/views/DreamInterpretation.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
