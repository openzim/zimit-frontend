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
    <div v-else>
      <p>{{ $t('blacklist.notPossible') }}</p>
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
