import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

import NotFound from './components/NotFound.vue'
import NewRequest from './components/NewRequest.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: {name: 'new'},
  },
  {
    path: '/new',
    name: 'new',
    component: NewRequest,
  },
  {
    path: '*',
    name: '404',
    component: NotFound
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  linkActiveClass: "active",
  linkExactActiveClass: "exact-active",
  routes:routes,
});

export default router;
