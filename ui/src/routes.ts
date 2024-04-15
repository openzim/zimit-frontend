import { createWebHashHistory, createRouter } from 'vue-router';

import RequestStatus from './views/RequestStatus.vue';
import NotFound from './views/NotFound.vue';
import NewRequest from './views/NewRequest.vue';
import AboutView from './views/AboutView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: NewRequest,
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
  },
  {
    path: '/request/:taskId([a-zA-Z-0-9]*)',
    name: 'request',
    component: RequestStatus,
    props: true,
  },
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  linkActiveClass: 'active',
  linkExactActiveClass: 'exact-active',
  routes: routes,
});

export default router;
