import Vue from 'vue'
Vue.config.productionTip = false

// main dependencies
import VueRouter from 'vue-router'

Vue.use(VueRouter);

// Bootstrap
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

import '../public/styles.css'

// Sugar extensions
import Sugar from 'sugar'
Sugar.extend({namespaces: [Array, Object]});

// Own modules
import App from './App.vue'
import Constants from './constants.js'
import router from './routes'
import store from './store'  // Vuex store

// Own filters
Vue.filter('filesize', Constants.filesize);
Vue.filter('format_dt', Constants.format_dt);
Vue.filter('from_now', Constants.from_now);
Vue.filter('duration', Constants.format_duration);
Vue.filter('yes_no', Constants.yes_no);
Vue.filter('short_id', Constants.short_id);


// matomo (stats.kiwix.org)
import VueMatomo from 'vue-matomo'
Vue.use(VueMatomo, {
  host: 'https://stats.kiwix.org',
  siteId: 11,
  trackerFileName: 'matomo',
  router: router,
});

new Vue({
  store: store,
  router: router,
  render: h => h(App),
}).$mount('#app')
