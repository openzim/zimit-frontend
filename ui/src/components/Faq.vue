<template>
  <div class="faq" role="tablist">
    <FaqEntry
      id="what-is-zim"
      :title="$t('faq.whatIsZim')">
      <template v-slot:default>
        {{ $t('faq.whatIsZimDesc') }}
      </template>
    </FaqEntry>

    <FaqEntry
      id="how-to-read"
      :title="$t('faq.howToRead')">
      <template v-slot:default>
        {{ $t('faq.howToReadDesc') }}
      </template>
    </FaqEntry>

    <FaqEntry
      id="missing-content"
      :title="$t('faq.missingContent')">
      <template v-slot:default>
        {{ $t('faq.missingContentDesc', { human_size_limit: human_size_limit, human_time_limit: human_time_limit }) }}
      </template>
    </FaqEntry>

    <FaqEntry
      id="got-error"
      :title="$t('faq.gotError')">
      <template v-slot:default>
        {{ $t('faq.gotErrorDesc') }}
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
      return this.$t('units.sizeLimit', { value: sizeInGiB });
    },
    human_time_limit() {
      const timeInHours = parseInt(Constants.zimit_time_limit / 3600);
      return this.$t('units.timeLimit', { value: timeInHours });
    },
  }
}
</script>