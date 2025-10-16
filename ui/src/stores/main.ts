import axios, { AxiosError } from 'axios'
import { defineStore } from 'pinia'

import constants from '../constants'
import { getCurrentLocale, setCurrentLocale, type Language } from '../i18n'

export type RootState = {
  count: number
  loading: boolean
  loadingText: string
  offlinerDefinition: OfflinerDefinition | undefined
  offlinerNotFound: boolean
  formValues: NameValue[]
  taskId: string
  taskData: TaskData | undefined
  taskNotFound: boolean
  snackbarDisplayed: boolean
  snackbarContent: string
  trackerStatus: TrackerStatusResponse | undefined
  blacklistReason: BlacklistEntry | undefined
}

export type LoadingPayload = {
  loading: boolean
  text?: string
}

export type OfflinerDefinition = {
  flags: OfflinerFlag[]
  help: string
}

export type OfflinerFlag = {
  data_key: string
  description: string
  key: string
  label: string
  required: boolean
  type: string
  choices: string[]
}

export type NameValue = {
  name: string
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  value: any
}

export type TrackerStatusResponse = {
  status: string
  ongoingTasks: string[] | undefined
}

export type PostRequestResponse = {
  id: string
  newUniqueId: string | undefined
}

export type TaskData = {
  id: string
  flags: NameValue[]
  // config: TaskDataConfig
  // // eslint-disable-next-line @typescript-eslint/no-explicit-any
  // container: any
  status: string
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  // files: any
  // filesParsed: TaskDataFile[]
  hasEmail: boolean
  partialZim: boolean
  downloadLink: string
  progress: number
  rank: number | undefined
  offlinerDefinitionVersion: string
}

export type BlacklistEntry = {
  host: string
  reason: string
  libraryUrl: string | null
  githubIssue: string | null
  scraperUrl: string | null
  wp1Hint: boolean | null
}

export interface Paginator {
  count: number
  skip: number
  limit: number
  page_size: number
  page: number
}

export interface ListResponse<T> {
  meta: Paginator
  items: T[]
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      count: 0,
      loading: false,
      loadingText: '',
      offlinerDefinition: undefined,
      offlinerNotFound: false,
      formValues: [] as NameValue[],
      taskId: '',
      taskData: undefined,
      taskNotFound: false,
      snackbarDisplayed: false,
      snackbarContent: '',
      trackerStatus: undefined,
      blacklistReason: undefined
    }) as RootState,
  actions: {
    setCurrentLocale(locale: Language) {
      setCurrentLocale(locale)
    },
    async loadTaskId(taskIds: string | string[]) {
      if (taskIds != this.taskId) {
        // for some reason, route param might be an array even if it is not possible in our setup
        const taskId = Array.isArray(taskIds) ? taskIds[0] : taskIds
        this.taskId = taskId
      }
      this.setLoading({
        loading: true,
        text: this.t('requestStatus.refreshing')
      })
      try {
        this.taskData = (
          await axios.get<TaskData>(this.config.zimit_ui_api + '/requests/' + this.taskId)
        ).data
        this.taskNotFound = false
      } catch (error) {
        this.handleError(this.t('requestStatus.errorRefreshing'), error)
        this.taskNotFound = true
      } finally {
        this.setLoading({ loading: false })
      }
    },
    setLoading(payload: LoadingPayload) {
      //toggle GUI loader
      this.loading = payload.loading
      this.loadingText = payload.text ? payload.text : ''
    },
    saveOfflinersDefinitions(offlinersDefinitions: OfflinerDefinition) {
      this.offlinerDefinition = offlinersDefinitions
    },

    increment() {
      this.count++
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    setFormValue(name: string, value: any) {
      const formValue = this.formValues.find((formValue) => formValue.name === name)
      if (!value || value === constants.not_set_magic_value) {
        if (formValue) {
          this.formValues.splice(this.formValues.indexOf(formValue))
        }
      } else {
        if (formValue) {
          formValue.value = value
        } else {
          this.formValues.push({ name: name, value: value } as NameValue)
        }
      }
    },
    async loadOfflinerDefinition() {
      try {
        const offlinerDefinition = (
          await axios.get<OfflinerDefinition>(this.config.zimit_ui_api + '/offliner-definition')
        ).data
        this.offlinerDefinition = offlinerDefinition
        this.offlinerNotFound = false
      } catch (error) {
        this.handleError(this.t('newRequest.errorFetchingDefinition'), error)
        this.offlinerNotFound = true
      }
    },
    async getTrackerStatus() {
      try {
        const response = (
          await axios.post<TrackerStatusResponse>(this.config.zimit_ui_api + '/tracker_status', {
            uniqueId: localStorage.getItem('uniqueId')
          })
        ).data
        this.trackerStatus = response
        if (this.trackerStatus.status == 'invalid_unique_id') {
          localStorage.removeItem('uniqueId')
          const response = (
            await axios.post<TrackerStatusResponse>(this.config.zimit_ui_api + '/tracker_status', {
              uniqueId: null
            })
          ).data
          this.trackerStatus = response
        }
      } catch (error) {
        this.handleError(this.t('newRequest.errorFetchingStatus'), error)
      }
    },
    async submitRequest() {
      const payload = {
        uniqueId: localStorage.getItem('uniqueId'),
        url: this.getFormValue('url'),
        lang: getCurrentLocale(),
        email: this.getFormValue('email'),
        flags: this.formValues
          .filter((flag) => this.config.new_request_advanced_flags.indexOf(flag.name) > -1)
          .reduce(
            (acc, flag) => {
              acc[flag.name] = flag.value
              return acc
            },
            {} as { [key: string]: string }
          )
      }
      this.setLoading({
        loading: true,
        text: this.t('newRequest.creatingRequest')
      })
      try {
        const response = (
          await axios.post<PostRequestResponse>(this.config.zimit_ui_api + '/requests', payload)
        ).data
        this.taskId = response.id
        if (response.newUniqueId) {
          localStorage.setItem('uniqueId', response.newUniqueId)
        }
        this.router.push({ name: 'request', params: { taskId: this.taskId } })
      } catch (error) {
        if (error instanceof AxiosError && error.response && error.response.status == 400) {
          this.blacklistReason = error.response.data['detail']['blacklist']
        } else {
          this.handleError(this.t('newRequest.errorCreatingRequest'), error)
        }
      } finally {
        this.setLoading({ loading: false })
      }
    },
    async cancelRequest() {
      const payload = {
        uniqueId: localStorage.getItem('uniqueId')
      }
      this.setLoading({
        loading: true,
        text: this.t('requestStatus.cancellingRequest')
      })
      try {
        await axios.post<PostRequestResponse>(
          `${this.config.zimit_ui_api}/requests/${this.taskId}/cancel`,
          payload
        )
        this.router.push({ name: 'home' })
      } catch (error) {
        this.handleError(this.t('requestStatus.errorCancellingRequest'), error)
      } finally {
        this.setLoading({ loading: false })
      }
    },
    handleError(message: string, error: unknown) {
      if (error instanceof AxiosError && error.response) {
        console.error(message, ':', error.response.status, error.response.statusText)
        if (error.response.data.detail) {
          message = message + ': ' + error.response.data.detail
        }
      } else {
        console.error(message, ':', error)
      }
      this.snackbarContent = message
      this.snackbarDisplayed = true
    }
  },
  getters: {
    loadingStatus(state) {
      return { shoudDisplay: state.loading, text: state.loadingText }
    },
    offlinerFlags(state) {
      return (
        state.offlinerDefinition?.flags.filter(
          (flag) => this.config.new_request_advanced_flags.indexOf(flag.data_key) > -1
        ) || []
      )
    },
    getFormValue: (state) => {
      return (name: string) => {
        const formValue = state.formValues.find((formValue) => formValue.name === name)
        if (formValue) {
          return formValue.value
        } else {
          return undefined
        }
      }
    },
    taskUrl(state) {
      if (!state.taskData) {
        return undefined
      }
      const urlFlags = state.taskData.flags.filter((flag) => flag.name == 'seeds')
      if (urlFlags.length !== 1) {
        return undefined
      }
      return urlFlags[0].value
    },
    taskRequested(state) {
      return state.taskData && state.taskData.status == 'requested'
    },
    taskSucceeded(state) {
      return state.taskData && state.taskData.status == 'succeeded'
    },
    taskCanceled(state) {
      return state.taskData && state.taskData.status == 'canceled'
    },
    taskCancelRequested(state) {
      return state.taskData && state.taskData.status == 'cancel_requested'
    },
    taskOngoing(): boolean {
      return this.taskSucceeded !== true && this.taskFailed !== true && this.taskCanceled !== true
    },
    taskEnded(): boolean {
      return !this.taskOngoing
    },
    taskFailed(state) {
      return state.taskData && ['failed', 'scraper_killed'].indexOf(state.taskData.status) != -1
    },
    taskProgression(): number {
      if (this.taskEnded) {
        return 100
      }
      return this.taskData ? this.taskData.progress : 0
    },
    taskSimpleStatus(state): string {
      if (this.taskRequested) return 'pending'
      if (this.taskOngoing) return 'in-progress'
      return state.taskData?.status || 'unknown'
    },
    taskHumanSizeLimit(state) {
      if (!state.taskData) {
        return undefined
      }
      const limitFlags = state.taskData.flags.filter((flag) => flag.name == 'sizeSoftLimit')
      if (limitFlags.length !== 1) {
        return undefined
      }
      const limitValue = limitFlags[0].value
      return Math.round((Number(limitValue) / 1073741824) * 10) / 10
    },
    taskHumanTimeLimit(state) {
      if (!state.taskData) {
        return undefined
      }
      const limitFlags = state.taskData.flags.filter((flag) => flag.name == 'timeSoftLimit')
      if (limitFlags.length !== 1) {
        return undefined
      }
      const limitValue = limitFlags[0].value
      return Math.round((Number(limitValue) / 3600) * 10) / 10
    }
  }
})
