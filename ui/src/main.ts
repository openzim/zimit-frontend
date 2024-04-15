import { createApp } from 'vue';
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

app.use(vuetify);

// Vue Router
import router from './routes';
app.use(router);

// Pinia
import { createPinia } from 'pinia';
const pinia = createPinia();
app.use(pinia);

// Final mount
app.mount('#app');

//console.log(import.meta.env.VITE_APP_TITLE)
// console.log(import.meta.env)
