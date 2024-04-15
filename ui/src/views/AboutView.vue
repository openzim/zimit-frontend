<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { setCurrentLocale } from '../i18n';

const { t } = useI18n();
setCurrentLocale('fa');
</script>

<template>About View: {{ t('faq.whatIsZim') }}</template>
