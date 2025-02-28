<script setup lang="ts">
import FaqList from '../components/FaqList.vue'
import NewRequestForm from '../components/NewRequestForm.vue'
import BlockRequest from '../components/BlockRequest.vue'
import { useI18n } from 'vue-i18n'
import { useMainStore } from '../stores/main'
import { onMounted } from 'vue'

const { t } = useI18n()
const mainStore = useMainStore()

onMounted(() => {
  Promise.all([
    mainStore.setLoading({
      loading: true,
      text: t('newRequest.fetchingDefinitionAndStatus')
    }),
    mainStore.loadOfflinerDefinition(),
    mainStore.getTrackerStatus()
  ]).then(() => {
    mainStore.setLoading({ loading: false })
  })
})
</script>

<template>
  <v-container id="newrequest" class="pt-0">
    <i18n-t keypath="newRequest.headingParagraph" tag="h1">
      <strong>{{ t('newRequest.headingBold') }}</strong>
    </i18n-t>
    <div v-if="mainStore.loading">
      {{ mainStore.loadingText }}
    </div>
    <div v-else-if="mainStore.offlinerNotFound" class="red">
      {{ $t('newRequest.offlinerNotFound') }}
    </div>
    <div v-else-if="mainStore.config.stop_new_requests_on">
      {{ $t('newRequest.stopNewRequestsMessage') }}
    </div>
    <div v-else-if="mainStore.trackerStatus?.status != 'can_add_task'">
      <BlockRequest />
    </div>
    <NewRequestForm v-else />
    <FaqList class="faq" />
  </v-container>
</template>

<style type="text/css" scoped>
#newrequest {
  max-width: 700px;
}

h1 {
  text-align: center;
  line-height: 1.2;
}

form {
  max-width: 700px;
  margin: auto;
}

.form-group,
h1 {
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 1.5em;
}

.faq {
  margin-top: 5rem;
  margin-bottom: 7rem;
}
</style>
