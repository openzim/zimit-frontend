import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import RequestStatus from "./components/RequestStatus.vue";
import NotFound from "./components/NotFound.vue";
import NewRequest from "./components/NewRequest.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: NewRequest,
  },
  {
    path: "/:taskId([a-z0-9]{24})",
    name: "request",
    component: RequestStatus,
    props: true,
  },
  {
    path: "*",
    name: "404",
    component: NotFound,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  linkActiveClass: "active",
  linkExactActiveClass: "exact-active",
  routes: routes,
});

export default router;
