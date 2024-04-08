<template>
  <div class="faq" role="tablist">
    <FaqEntry id="what-is-zim" :title="$t('faq.whatIsZim')">
      <template v-slot:default>
        <div v-html="$t('faq.whatIsZimDesc')"></div>
      </template>
    </FaqEntry>

    <FaqEntry id="how-to-read" :title="$t('faq.howToRead')">
      <template v-slot:default>
        <div v-html="$t('faq.howToReadDesc')"></div>
      </template>
    </FaqEntry>

    <FaqEntry id="missing-content" :title="$t('faq.missingContent')">
      <template v-slot:default>
        {{ $t('faq.missingContentDesc', { 
          human_size_limit: human_size_limit,
          human_time_limit: human_time_limit + ' ' + (human_time_limit === 1 ? $t('units.timeLimit.singular') : $t('units.timeLimit.plural'))
        }) }}
      </template>
    </FaqEntry>

    <FaqEntry id="got-error" :title="$t('faq.gotError')">
      <template v-slot:default>
        <div v-html="$t('faq.gotErrorDesc')"></div>
      </template>
    </FaqEntry>
  </div>
</template>

<script type="text/javascript">
import FaqEntry from './FaqEntry.vue'
import Constants from '../constants.js'

export default {
  name: 'Faq',
  components: { FaqEntry },
  computed: {
    human_size_limit() {
      const sizeInGiB = parseInt(Constants.zimit_size_limit / 1073741824);
      return `${sizeInGiB} GiB`;
    },
    human_time_limit() {
      const timeInHours = parseInt(Constants.zimit_time_limit / 3600);
      return timeInHours;
    },
  }
}
</script>