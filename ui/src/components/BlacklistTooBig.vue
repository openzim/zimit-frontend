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
      <p>{{ $t('blacklist.tooBig.tooBigDetails') }}</p>
      <p>{{ $t('blacklist.tooBig.alreadyMadeZim') }}</p>
      <i18n-t keypath="blacklist.tooBig.downloadOrRequest" tag="p">
        <template #libraryLink>
          <a :href="mainStore.blacklistReason.libraryUrl" target="_blank">{{
            $t('blacklist.tooBig.libraryLinkContent')
          }}</a>
        </template>
        <template #githubRequestLink>
          <a
            href="https://github.com/openzim/zim-requests/issues/new?template=new-zim-request.md"
            target="_blank"
            >{{ $t('blacklist.tooBig.githubRequestLinkContent') }}</a
          >
        </template>
      </i18n-t>
      <i18n-t
        v-if="mainStore.blacklistReason.scraperUrl"
        keypath="blacklist.tooBig.useScraper"
        tag="p"
      >
        <template #scraperRepoLink>
          <a :href="mainStore.blacklistReason.scraperUrl" target="_blank">{{
            $t('blacklist.tooBig.scraperRepoLinkContent')
          }}</a>
        </template>
      </i18n-t>
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
