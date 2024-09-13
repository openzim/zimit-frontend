import { createWebHashHistory, createRouter } from 'vue-router'
import type { Router } from 'vue-router'
import type { PiniaPluginContext } from 'pinia'

import RequestStatus from './views/RequestStatus.vue'
import NotFound from './views/NotFound.vue'
import NewRequest from './views/NewRequest.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: NewRequest
  },
  {
    path: '/request/:taskId([a-zA-Z-0-9]*)',
    name: 'request',
    component: RequestStatus
  },
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  linkActiveClass: 'active',
  linkExactActiveClass: 'exact-active',
  routes: routes
})

declare module 'pinia' {
  export interface PiniaCustomProperties {
    router: Router
  }
}

export function routerPlugin({ store }: PiniaPluginContext) {
  store.router = router
}

export default router
