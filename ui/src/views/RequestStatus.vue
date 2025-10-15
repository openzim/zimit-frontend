<script setup lang="ts">
import { inject, onBeforeUnmount, onMounted, watch } from 'vue'
import type { Config } from '../config'
import constants from '../constants'
import type { OfflinerDefinition } from '../stores/main'

import { useRoute } from 'vue-router'
const route = useRoute()

import { useMainStore } from '../stores/main'
const mainStore = useMainStore()

const config = inject<Config>(constants.config)

let refreshInterval: ReturnType<typeof setInterval> | undefined

const getKeyLabel = (key: string, offlinerDefinition: OfflinerDefinition) => {
  const flag = offlinerDefinition.flags.find((flag) => flag.key == key || flag.data_key == key)
  return flag?.label
}

onMounted(() => {
  Promise.all([mainStore.getTrackerStatus(), mainStore.loadTaskId(route.params.taskId)])

  // Reload task periodically
  if (!config) {
    console.error('Impossible to setup periodic refresh without config')
    return
  }
  refreshInterval = setInterval(() => {
    mainStore.loadTaskId(mainStore.taskId)
  }, config.zimit_refresh_after * 1000)
})

onBeforeUnmount(() => {
  if (refreshInterval) {
    // Clear the interval to avoid memory leaks
    clearInterval(refreshInterval)
  }
})

watch(
  () => route.params.taskId,
  (newValue) => mainStore.loadTaskId(newValue)
)
</script>

<template>
  <v-container id="newrequest">
    <div>
      <i18n-t keypath="requestStatus.refreshAuto" tag="p">
        <template #refresh_interval>
          {{ config?.zimit_refresh_after }}
        </template>
      </i18n-t>

      <p v-if="mainStore.loading">{{ mainStore.loadingText }}</p>
    </div>
    <div v-if="mainStore.taskData">
      <h1>
        {{ $t('requestStatus.zimingOf')
        }}<a :href="mainStore.taskUrl" target="_blank">{{ mainStore.taskUrl }}</a>
      </h1>
      <div
        v-if="mainStore.trackerStatus?.ongoingTasks?.includes(mainStore.taskId)"
        id="cancel"
        @click="mainStore.cancelRequest()"
      >
        <v-btn color="red">{{ $t('requestStatus.cancelButton') }}</v-btn>
      </div>

      <v-progress-linear
        v-model="mainStore.taskProgression"
        height="25"
        striped
        :color="mainStore.taskSucceeded ? 'success' : mainStore.taskFailed ? 'error' : 'info'"
      >
        <i18n-t keypath="requestStatus.progressMessage" tag="strong">
          <template #task_progression_percent>
            {{ Math.ceil(mainStore.taskProgression) }}
          </template>
          <template #task_progression_status_code>
            {{ mainStore.taskSimpleStatus }}
          </template>
        </i18n-t>
      </v-progress-linear>

      <div v-if="mainStore.taskRequested" class="pt-4 pb-4">
        <v-alert :title="$t('requestStatus.requestingSlot')" color="warning" variant="tonal">
          <template #text>
            <p>{{ $t('requestStatus.requestRecorded') }}</p>
            <i18n-t v-if="mainStore.taskData.rank" keypath="requestStatus.rankMessage" tag="strong">
              <template #task_rank>
                {{ mainStore.taskData.rank + 1 }}
              </template>
            </i18n-t>
            <p v-if="mainStore.taskData.hasEmail">{{ $t('requestStatus.bookmarkUrl') }}</p>
            <p v-if="mainStore.taskData.hasEmail">{{ $t('requestStatus.emailNotification') }}</p>
            <p v-else>{{ $t('requestStatus.noEmailNotification') }}</p>
          </template>
        </v-alert>
      </div>
      <div v-else-if="mainStore.taskCancelRequested" class="pt-4 pb-4">
        <v-alert :title="$t('requestStatus.requestCancelRequested')" color="error">
          <template #text>
            <p class="pt-2">{{ $t('requestStatus.requestCancelRequestedExplanation') }}</p>
          </template>
        </v-alert>
      </div>
      <div v-else-if="mainStore.taskCanceled" class="pt-4 pb-4">
        <v-alert :title="$t('requestStatus.requestCanceled')" color="error"> </v-alert>
      </div>
      <div v-else-if="mainStore.taskFailed" class="pt-4 pb-4">
        <v-alert :title="$t('requestStatus.requestFailed')" color="error">
          <template #text>
            <i18n-t keypath="requestStatus.failureReasons" tag="span">
              <a target="_blank" :href="mainStore.config.report_issues_page">{{
                $t('requestStatus.failureReasonsLinkContent0')
              }}</a>
            </i18n-t>
          </template>
        </v-alert>
      </div>
      <div v-else-if="mainStore.taskSucceeded" class="pt-4 pb-4">
        <v-alert :title="$t('requestStatus.successMessage')" color="success">
          <template #text>
            <p class="pt-2">{{ $t('requestStatus.successMessageExplanation') }}</p>
            <p class="pt-2">
              <v-btn rounded="xl" target="_blank" :href="mainStore.taskData.downloadLink">{{
                $t('requestStatus.successMessageButton')
              }}</v-btn>
            </p>

            <i18n-t
              v-if="mainStore.taskData.partialZim"
              keypath="requestStatus.partialZim"
              tag="p"
              class="pt-2"
            >
              <template #human_size_limit>
                {{ mainStore.taskHumanSizeLimit }}
              </template>
              <template #human_time_limit>
                {{
                  mainStore.taskHumanTimeLimit +
                  ' ' +
                  (mainStore.taskHumanTimeLimit === 1
                    ? $t('units.timeLimit.singular')
                    : $t('units.timeLimit.plural'))
                }}
              </template>
              <template #contact_us_link>
                <a target="_blank" :href="mainStore.config.kiwix_contact_us">{{
                  $t('requestStatus.partialZimContactUsLink')
                }}</a>
              </template>
            </i18n-t>
          </template>
        </v-alert>
      </div>
      <div v-else class="pt-4 pb-4">
        <v-alert :title="$t('requestStatus.beingProcessedMessage')" color="info">
          <template #text>
            <p>{{ $t('requestStatus.beingProcessedExplanation') }}</p>
            <p>{{ $t('requestStatus.bookmarkUrl') }}</p>
            <p v-if="mainStore.taskData.hasEmail">{{ $t('requestStatus.emailNotification') }}</p>
            <p v-else>{{ $t('requestStatus.noEmailNotification') }}</p>
          </template>
        </v-alert>
      </div>

      <h2>{{ $t('requestStatus.settingsHeading') }}</h2>
      <v-table>
        <tbody>
          <tr
            v-for="(flag, index) in mainStore.taskData.flags.filter(
              (flag) =>
                config?.task_status_hidden_flags.indexOf(flag.name) == -1 && flag.value !== null
            )"
            :key="flag.name"
            :class="{ 'striped-row': index % 2 === 0 }"
          >
            <th>{{ getKeyLabel(flag.name, mainStore.offlinerDefinition!) }}</th>
            <td>{{ flag.value }}</td>
          </tr>
        </tbody>
      </v-table>
    </div>
    <div v-if="mainStore.taskNotFound" class="red">
      {{ $t('requestStatus.taskNotFound') }}
    </div>
  </v-container>
</template>

<style type="text/css" scoped>
.striped-row {
  background-color: #f0f0f0;
}

th {
  width: 25%;
}

#cancel {
  margin: 1rem 0;
}

#newrequest {
  padding-bottom: 5rem;
}
</style>
