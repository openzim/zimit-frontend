<script setup lang="ts">
import FaqEntry from './FaqEntry.vue';
import Constants from '../constants.js';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

const { t } = useI18n();

const human_size_limit = computed(() => {
  return `${Constants.zimit_size_limit / 1073741824} GiB`;
});

const human_time_limit = computed(() => {
  return Constants.zimit_time_limit / 3600;
});
</script>

<template>
  <v-expansion-panels variant="accordion">
    <FaqEntry id="what-is-zim" :title="t('faq.whatIsZim')">
      <template #default>
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="t('faq.whatIsZimDesc')"></div>
      </template>
    </FaqEntry>

    <FaqEntry id="how-to-read" :title="t('faq.howToRead')">
      <template #default>
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="t('faq.howToReadDesc')"></div>
      </template>
    </FaqEntry>

    <FaqEntry id="missing-content" :title="t('faq.missingContent')">
      <template #default>
        {{
          t('faq.missingContentDesc', {
            human_size_limit: human_size_limit,
            human_time_limit:
              human_time_limit +
              ' ' +
              (human_time_limit === 1
                ? t('units.timeLimit.singular')
                : t('units.timeLimit.plural')),
          })
        }}
      </template>
    </FaqEntry>

    <FaqEntry id="got-error" :title="t('faq.gotError')">
      <template #default>
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="t('faq.gotErrorDesc')"></div>
      </template>
    </FaqEntry>
  </v-expansion-panels>
</template>
