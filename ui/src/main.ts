import { createApp } from 'vue';
import constants from './constants';
import './style.css';
import App from './App.vue';

const app = createApp(App);

// Font-Awesome
import { aliases, fa } from 'vuetify/iconsets/fa-svg';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
app.component('font-awesome-icon', FontAwesomeIcon); // Register component globally
library.add(fas); // Include needed solid icons
library.add(far); // Include needed regular icons

// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'fa',
    aliases,
    sets: {
      fa,
    },
  },
});

// Pinia
import { createPinia } from 'pinia';
const pinia = createPinia();

// Vue Router
import router from './routes';

// i18n
import loadI18n from './i18n';

// load translation asynchronously and only then mount the app
loadI18n().then((loadI18n) => {
  app.use(vuetify);
  app.use(router);
  app.use(pinia);
  app.use(loadI18n.i18n);

  // provide setCurrentLocale function app-wide, so that we can
  // alter the locale in any app view/component
  app.provide(constants.setCurrentLocale, loadI18n.setCurrentLocale);

  // Final mount
  app.mount('#app');
});

//console.log(import.meta.env.VITE_APP_TITLE)
// console.log(import.meta.env)
