<script setup lang="ts">
import FaqEntry from './FaqEntry.vue';
import constants from '../constants.js';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

const { t } = useI18n();

const human_size_limit = computed(() => {
  return `${constants.zimit_size_limit / 1073741824} GiB`;
});

const human_time_limit = computed(() => {
  return constants.zimit_time_limit / 3600;
});
</script>

<template>
  <v-expansion-panels flat variant="accordion">
    <FaqEntry id="what-is-zim" :title="t('faq.whatIsZim')">
      <template #default>
        <i18n-t keypath="faq.whatIsZimDescParagraph" tag="div">
          <a target="_blank" :href="constants.wikipedia_offline_article">{{
            t('faq.whatIsZimDescLinkContent0')
          }}</a>
        </i18n-t>
      </template>
    </FaqEntry>

    <FaqEntry id="how-to-read" :title="t('faq.howToRead')">
      <template #default>
        <i18n-t keypath="faq.howToReadDescParagraph" tag="div">
          <a target="_blank" :href="constants.kiwix_home_page">{{
            t('faq.howToReadDescLinkContent0')
          }}</a>
          <a target="_blank" :href="constants.kiwix_download_page">{{
            t('faq.howToReadDescLinkContent1')
          }}</a>
        </i18n-t>
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
        <i18n-t keypath="faq.gotErrorDescParagraph" tag="div">
          <a target="_blank" :href="constants.report_issues_page">{{
            t('faq.gotErrorDescLinkContent0')
          }}</a>
        </i18n-t>
      </template>
    </FaqEntry>
  </v-expansion-panels>
</template>
