import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'

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

export type PostRequestResponse = {
  id: string
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
  limitHit: boolean
  downloadLink: string
  progress: number
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
      snackbarContent: ''
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
      this.setLoading({
        loading: true,
        text: this.t('newRequest.fetchingDefinition')
      })
      try {
        const offlinerDefinition = (
          await axios.get<OfflinerDefinition>(this.config.zimfarm_api + '/offliners/zimit')
        ).data
        offlinerDefinition.flags = offlinerDefinition.flags.filter(
          (flag) => this.config.new_request_advanced_flags.indexOf(flag.key) > -1
        )
        this.offlinerDefinition = offlinerDefinition
        this.offlinerNotFound = false
      } catch (error) {
        this.handleError(this.t('newRequest.errorFetchingDefinition'), error)
        this.offlinerNotFound = true
      } finally {
        this.setLoading({ loading: false })
      }
    },
    async submitRequest() {
      const payload = {
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
        this.router.push({ name: 'request', params: { taskId: this.taskId } })
      } catch (error) {
        this.handleError(this.t('newRequest.errorCreatingRequest'), error)
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
      return state.offlinerDefinition?.flags || []
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
      const urlFlags = state.taskData.flags.filter((flag) => flag.name == 'url')
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
    taskOngoing(): boolean {
      return this.taskSucceeded !== true && this.taskFailed !== true
    },
    taskEnded(): boolean {
      return !this.taskOngoing
    },
    taskFailed(state) {
      return (
        state.taskData &&
        ['canceled', 'cancel_requested', 'failed', 'scraper_killed'].indexOf(
          state.taskData.status
        ) != -1
      )
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
      const limitFlags = state.taskData.flags.filter((flag) => flag.name == 'sizeLimit')
      if (limitFlags.length !== 1) {
        return undefined
      }
      const limitValue = limitFlags[0].value
      return Number(limitValue) / 1073741824
    },
    taskHumanTimeLimit(state) {
      if (!state.taskData) {
        return undefined
      }
      const limitFlags = state.taskData.flags.filter((flag) => flag.name == 'timeLimit')
      if (limitFlags.length !== 1) {
        return undefined
      }
      const limitValue = limitFlags[0].value
      return Number(limitValue) / 3600
    }
  }
})
