import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import BabyPage from '../components/BabyPage.vue';

const routes = [
  { path: '/', component: LoginPage },
  { path: '/user/:userId', name: 'BabyPage', component: BabyPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;