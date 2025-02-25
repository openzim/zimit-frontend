<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useMainStore } from '../stores/main'

const { t } = useI18n()
const mainStore = useMainStore()
</script>

<template>
  <div v-if="!mainStore.trackerStatus">
    <!--Never supposed to get here-->
    <p>You are blocked but we miss the detailed reason</p>
    <p>Please contact us if the situation persist.</p>
  </div>
  <div v-else-if="mainStore.trackerStatus.status='too_many_tasks_for_unique_id'">
    <p>Zimit being a free service, we limit the number of tasks per user.</p>
    <p>You have reached your quota, please wait for tasks to complete or contact us if you want more quota.</p>
    <p>Please use links below to monitor / cancel ongoing tasks.</p>
    <p v-for="ongoingTask in mainStore.trackerStatus.ongoingTasks" :key="ongoingTask">Go to ongoing task {{ ongoingTask }}</p>
  </div>
  <div v-else-if="mainStore.trackerStatus.status='too_many_tasks_for_ip_address'">
    <p>Zimit being a free service, we limit the number of tasks per user.</p>
    <p>We've detect excessive usage from your environment, please come back in few hours.</p>
    <p>Please contact us if the situation persist.</p>
  </div>
  <div v-else>
    <!--Never supposed to get here-->
    <p>You are blocked for abnormal usage: {{ mainStore.trackerStatus.status }}</p>
    <p>Please contact us if the situation persist.</p>
  </div>
</template>

<style type="text/css" scoped>

p {
    margin-bottom: 1rem;
}
</style>
