<script setup lang="ts">
import { inject, computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Config } from './config'
import constants from './constants'
import { supportedLanguages, getCurrentLocale, setCurrentLocale } from './i18n'
const { t } = useI18n()
const config = inject<Config>(constants.config)
import { useDisplay } from 'vuetify'

import { useMainStore } from './stores/main'
const mainStore = useMainStore()

const { smAndDown } = useDisplay()

// compute items for language combobox
const languageItems = computed(() => {
  return supportedLanguages
    .map((lang) => {
      return { title: lang.display, langCode: lang.code }
    })
    .sort((a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase()))
})

// and select appropriate one as default value for combobox initialization
const selectedLanguageItem = ref(
  languageItems.value.filter((langItem) => langItem.langCode == getCurrentLocale())[0]
)

// and select underlying "real" language object
const selectedLanguage = ref(
  supportedLanguages.find((lang) => lang.code == selectedLanguageItem.value.langCode) ||
    supportedLanguages[0]
)

watch(
  () => selectedLanguageItem.value,
  (newValue) => {
    selectedLanguage.value =
      supportedLanguages.find((lang) => lang.code == newValue.langCode) || supportedLanguages[0]
    setCurrentLocale(selectedLanguage.value)
  }
)
</script>

<template>
  <!-- Force LTR/RTL on whole app, we do not use vuetify locales at all -->
  <v-locale-provider :rtl="selectedLanguage.rtl">
    <div class="text-center" :class="smAndDown ? 'logo-div-sm' : 'logo-div'">
      <a :href="config?.home_page" target="_blank">
        <img src="./assets/ZIMIT_LOGO_RGB.svg" class="logo-img vue" alt="Vue logo" />
      </a>
    </div>
    <div class="top-corner">
      <v-btn
        class="donate-btn btn-green-rev"
        append-icon="fa-gift"
        variant="outlined"
        size="large"
        href="https://kiwix.org/en/get-involved/#donate"
        target="_blank"
      >
        {{ t('header.donate') }}
      </v-btn>
      <v-select
        v-model="selectedLanguageItem"
        class="language-select pt-2"
        :items="languageItems"
        density="compact"
        return-object
      >
      </v-select>
    </div>
    <RouterView />
    <i18n-t keypath="footer.poweredByThankTo" tag="footer" class="text-center">
      <a target="_blank" href="https://kiwix.org">{{ t('footer.link0') }}</a>
      <a target="_blank" href="https://webrecorder.net">{{ t('footer.link1') }}</a>
      <a target="_blank" href="https://www.mozilla.org/moss/">{{ t('footer.link2') }}</a>
    </i18n-t>
    <v-snackbar v-model="mainStore.snackbarDisplayed" color="red">
      {{ mainStore.snackbarContent }}
    </v-snackbar>
  </v-locale-provider>
</template>

<style scoped>
footer {
  background-color: #fff;
  z-index: 1;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  padding-top: 1em;
  padding-bottom: 1em;
}

.logo-img {
  width: 400px;
}

.logo-div {
  padding-top: 2em;
  padding-bottom: 2em;
}

.logo-div-sm {
  padding-top: 8em;
  padding-bottom: 2em;
}

.top-corner {
  position: absolute;
  top: 10px;
  inset-inline-end: 10px;
  z-index: 999;
  min-width: 10rem;
  display: flex;
  flex-direction: column;
  align-items: end;
}

.donate-btn {
  text-transform: none;
  border-color: black;
  border-width: 2px;
  color: #82ca2a;
}
</style>
