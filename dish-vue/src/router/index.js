import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import BabyPage from '../components/BabyPage.vue';
import AddDishPage from '../components/AddDishPage.vue';
import HistoryDishPage from '../components/HistoryDishPage.vue';
import PersonalPage from '../components/PersonalPage.vue';
// import APPIF from '@/APPIF.vue';

const routes = [
  { path: '/', component: LoginPage },
  // { path: '/', component: APPIF },
  { path: '/user/:userId', name: 'BabyPage', component: BabyPage },
  { path: '/add-dish/:userId', name: 'AddDishPage', component: AddDishPage },
  { path: '/history-dish/:userId', name: 'HistoryDishPage', component: HistoryDishPage },
  { path: '/personal-page/:userId', name: 'PersonalPage', component: PersonalPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
