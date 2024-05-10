import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import UserProfilePage from '../components/UserProfilePage.vue';

const routes = [
  { path: '/', component: LoginPage },
  { path: '/user/:userId', name: 'UserProfile', component: UserProfilePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;