<script setup lang="ts">
import FaqList from '../components/FaqList.vue'
import NewRequestForm from '../components/NewRequestForm.vue'
import { useI18n } from 'vue-i18n'
import { useMainStore } from '../stores/main'
import { onMounted } from 'vue'

const { t } = useI18n()
const mainStore = useMainStore()

onMounted(() => {
  mainStore.loadOfflinerDefinition()
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
    <div v-if="mainStore.offlinerNotFound" class="red">
      {{ $t('newRequest.offlinerNotFound') }}
    </div>
    <NewRequestForm />
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
