/* Declare what we use in vue-matomo (this is far from complete but sufficient for our
 usage, so that TypeScript compiler can check what needs to be) */
declare module 'vue-matomo' {
  import { PluginFunction } from 'vue'

  interface VueMatomoOptions {
    host: string
    siteId: number
    trackerFileName?: string
    router: Router
  }

  const VueMatomo: {
    install: PluginFunction<VueMatomoOptions>
  }

  export default VueMatomo
}
