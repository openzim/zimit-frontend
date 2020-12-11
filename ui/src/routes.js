import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

import Request from './components/Request.vue'
import Faq from './components/Faq.vue'
import NotFound from './components/NotFound.vue'
import NewRequest from './components/NewRequest.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: NewRequest,
  },
  {
    path: '/faq',
    name: 'faq',
    component: Faq,
  },
  {
    path: '/:task_id([a-z0-9]{24})',
    name: 'request',
    component: Request,
    props: true,

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
