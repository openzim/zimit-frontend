<script setup lang="ts">
import { useMainStore } from '../stores/main'

const mainStore = useMainStore()
</script>

<template>
  <div v-if="!mainStore.trackerStatus">
    <!--Never supposed to get here-->
    <p>{{ $t('blockedRequest.blockedMissingReason') }}</p>
    <p>{{ $t('blockedRequest.contactUsIfPersist') }}</p>
  </div>
  <div v-else-if="mainStore.trackerStatus.status == 'too_many_tasks_for_unique_id'">
    <p>{{ $t('blockedRequest.zimitFreeService') }}</p>
    <p>{{ $t('blockedRequest.quotaReached') }}</p>
    <p>{{ $t('blockedRequest.useLinksBelowToSeeTask') }}</p>
    <p v-for="ongoingTask in mainStore.trackerStatus.ongoingTasks" :key="ongoingTask">
      <i18n-t keypath="blockedRequest.goToTask" tag="p">
        <template #taskLink>
          <RouterLink :to="`/request/${ongoingTask}`">{{ ongoingTask }}</RouterLink>
        </template>
      </i18n-t>
    </p>
  </div>
  <div v-else-if="mainStore.trackerStatus.status == 'too_many_tasks_for_ip_address'">
    <p>{{ $t('blockedRequest.zimitFreeService') }}</p>
    <p>{{ $t('blockedRequest.excessiveUsage') }}</p>
    <p>{{ $t('blockedRequest.contactUsIfPersist') }}</p>
  </div>
  <div v-else>
    <!--Never supposed to get here-->
    <i18n-t keypath="blockedRequest.abnormalUsage" tag="p">
      <template #status>
        {{ mainStore.trackerStatus.status }}
      </template>
    </i18n-t>
    <p>{{ $t('blockedRequest.contactUsIfPersist') }}</p>
  </div>
</template>

<style type="text/css" scoped>
p {
  margin-bottom: 1rem;
}
</style>
