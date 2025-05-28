import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import Auth from "@/views/Auth.vue";
import HomePage from "@/views/Main.vue";
import { useMainStore } from '../store';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/auth'
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth,
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const store = useMainStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  if (requiresAuth && !store.isAuthenticated) {
    next('/auth');
  } else if (requiresAuth && store.isAuthenticated && to.path === '/auth') {
    next('/home');
  } else {
    next();
  }
});

export default router;