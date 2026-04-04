import { createRouter, createWebHistory } from 'vue-router'
import Search from '../views/Search.vue'
import About from '../views/About.vue'
import Random from '../views/Random.vue'
import Donate from '../views/Donate.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    redirect: '/search'
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/random',
    name: 'Random',
    component: Random
  },
  {
    path: '/donate',
    name: 'Donate',
    component: Donate
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router