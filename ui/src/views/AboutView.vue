<script setup lang="ts">
import { useI18n } from 'vue-i18n';
// import i18n from '../i18n';
import { inject } from 'vue';
const { t } = useI18n();

import constants from '../constants';

const setCurrentLocale = inject(constants.setCurrentLocale);

if (setCurrentLocale) {
  setCurrentLocale('fa');
}
</script>

<template>About View: {{ t('faq.whatIsZim') }}</template>
