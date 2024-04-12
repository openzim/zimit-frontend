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
Sugar.extend({namespaces: [Array, Object, Number]});

// vue-i18n integration starts here
import VueI18n from 'vue-i18n';
Vue.use(VueI18n);

// Assuming you have a locales directory with en.json and fr.json for example
function loadLocaleMessages() {
  const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
  const messages = {}
  locales.keys().forEach(key => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i)
    if (matched && matched.length > 1) {
      const locale = matched[1]
      messages[locale] = locales(key)
    }
  })
  return messages
}

// Detect browser language
const browserLanguage = navigator.language || navigator.userLanguage;

const simplifiedBrowserLanguage = browserLanguage.split('-')[0];

const supportedLanguages = ['en', 'fr']; // Add more supported languages here

const defaultLanguage = supportedLanguages.includes(simplifiedBrowserLanguage) ? simplifiedBrowserLanguage : 'en';

const i18n = new VueI18n({
  locale: defaultLanguage, // set locale
  fallbackLocale: 'en', // set fallback locale
  messages: loadLocaleMessages(), // set locale messages
});

// Own modules
import App from './App.vue'
import Constants from './constants.js'
import router from './routes'
import store from './store'  // Vuex store

// Own filters
Vue.filter('yes_no', Constants.yes_no);

// matomo (stats.kiwix.org)
import VueMatomo from 'vue-matomo'
Vue.use(VueMatomo, {
  host: 'https://stats.kiwix.org',
  siteId: 11,
  trackerFileName: 'matomo',
  router: router,
});

new Vue({
  router,
  store,
  i18n,
  render: h => h(App),
  created() {
    this.setPageDirection(this.$i18n.locale);
  },
  methods: {
    setPageDirection(locale) {
      const dir = locale === 'fa' ? 'rtl' : 'ltr';
      document.documentElement.setAttribute('dir', dir);
    },
  },
  watch: {
    '$i18n.locale'(newLocale) {
      this.setPageDirection(newLocale);
    },
  },
}).$mount('#app');
