import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/MainPage.vue'
import StubPage from '../pages/StubPage.vue'

const routes = [
  { path: '/', name: 'main', component: MainPage },
  { path: '/feed', name: 'feed', component: MainPage },
  { path: '/stub', name: 'stub', component: StubPage },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router

