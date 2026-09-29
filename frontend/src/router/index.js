import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router';
import Welcome from '@/views/Welcome.vue';
import Home from '@/views/Home.vue';
import Posts from '@/views/Posts.vue';
import Tools from '@/views/Tools.vue';
import About from '@/views/About.vue';
import Footprints from '@/views/Footprints.vue';
import AppPage from '@/views/App.vue';

const routes = [
  { path: '/', name: 'Welcome', component: Welcome, meta: { keepAlive: false } },
  { path: '/home', name: 'Home', component: Home },
  { path: '/docs', redirect: '/home' },
  { path: '/posts', name: 'Posts', component: Posts },
  { path: '/footprints', name: 'Footprints', component: Footprints },
  { path: '/tools', name: 'Tools', component: Tools },
  { path: '/about', name: 'About', component: About },
  { path: '/app', name: 'App', component: AppPage },
  { path: '/65472console', redirect: '/posts' },
];

const router = createRouter({
  history: import.meta.env.VITE_USE_HASH_ROUTER === 'true'
    ? createWebHashHistory(import.meta.env.BASE_URL)
    : createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
