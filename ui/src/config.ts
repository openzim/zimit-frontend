import axios from 'axios'
import { inject } from 'vue'
import type { PiniaPluginContext } from 'pinia'
import constants from './constants'

export type Config = {
  zimit_ui_api: string
  zimfarm_api: string
  wikipedia_offline_article: string
  kiwix_home_page: string
  kiwix_download_page: string
  kiwix_contact_us: string
  report_issues_page: string
  home_page: string
  zim_download_url: string
  new_request_advanced_flags: Array<string>
  task_status_hidden_flags: Array<string>
  zimit_size_limit: number
  zimit_time_limit: number
  zimit_refresh_after: number
}

async function loadConfig() {
  return (await axios.get<Config>('/config.json')).data
}

declare module 'pinia' {
  export interface PiniaCustomProperties {
    config: Config
  }
}

export function configPlugin({ store }: PiniaPluginContext) {
  const config = inject<Config>(constants.config)
  if (config) {
    store.config = config
  }
}

export default loadConfig
