<script setup lang="ts">
import { useMainStore } from '../stores/main'
const mainStore = useMainStore()

const close = function () {
  mainStore.blacklistReason = undefined
}
</script>

<template>
  <div class="main">
    <div v-if="!mainStore.blacklistReason">{{ $t('blacklist.missingReason') }}</div>
    <div v-else-if="!mainStore.blacklistReason.libraryUrl">
      {{ $t('blacklist.missingLibraryUrl') }}
    </div>
    <div v-else>
      <p>{{ $t('blacklist.alreadyZimed.alreadyMadeZim') }}</p>
      <i18n-t keypath="blacklist.alreadyZimed.downloadFromLibrary" tag="p">
        <template #link>
          <a :href="mainStore.blacklistReason.libraryUrl" target="_blank">{{
            $t('blacklist.alreadyZimed.downloadFromLibraryLinkContent')
          }}</a>
        </template>
      </i18n-t>
      <i18n-t
        v-if="mainStore.blacklistReason.wp1Hint"
        keypath="blacklist.alreadyZimed.wp1Hint"
        tag="p"
      >
        <template #wp1Link>
          <a href="https://wp1.openzim.org/#/selections/simple" target="_blank">{{
            $t('blacklist.alreadyZimed.wp1LinkContent')
          }}</a>
        </template>
      </i18n-t>
      <p>{{ $t('blacklist.contactUs') }}</p>
    </div>
    <v-btn class="black" rounded="xl" @click="close">{{ $t('blacklist.goBack') }}</v-btn>
  </div>
</template>

<style type="text/css" scoped>
.v-btn {
  text-transform: none;
  background-color: transparent;
}

.v-btn.black {
  background-color: black;
  color: white;
}

p {
  margin-bottom: 1rem;
}

.main {
  text-align: center;
}
</style>
