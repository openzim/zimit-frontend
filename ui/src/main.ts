import { createApp } from 'vue'
import constants from './constants'
import './style.css'
import App from './App.vue'

const app = createApp(App)

// Font-Awesome
import { aliases, fa } from 'vuetify/iconsets/fa-svg'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
// eslint-disable-next-line vue/component-definition-name-casing
app.component('font-awesome-icon', FontAwesomeIcon) // Register component globally
library.add(fas) // Include needed solid icons
library.add(far) // Include needed regular icons

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'fa',
    aliases,
    sets: {
      fa
    }
  }
})

// Pinia
import { createPinia } from 'pinia'
const pinia = createPinia()

// Vue Router
import router, { routerPlugin } from './routes'

// i18n
import loadI18n, { i18nPlugin } from './i18n'

// config
import loadConfig, { configPlugin } from './config'

// load translation asynchronously and only then mount the app
Promise.all([loadI18n(), loadConfig()]).then(([i18n, config]) => {
  app.use(vuetify)
  app.use(router)
  app.use(pinia)
  app.use(i18n)

  // provide config app-wide
  app.provide(constants.config, config)

  // inject plugins into store
  pinia.use(configPlugin)
  pinia.use(routerPlugin)
  pinia.use(i18nPlugin)

  // Final mount
  app.mount('#app')
})
