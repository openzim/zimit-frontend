<template>
  <div class="faq" role="tablist">
    <FaqEntry
      id="what-is-zim"
      :title="$t('faq.whatIsZim')"
      :content="$t('faq.whatIsZimDesc')">
    </FaqEntry>

    <FaqEntry
      id="how-to-read"
      :title="$t('faq.howToRead')"
      :content="$t('faq.howToReadDesc')">
    </FaqEntry>

    <FaqEntry
      id="missing-content"
      :title="$t('faq.missingContent')"
      :content="$t('faq.missingContentDesc', { human_size_limit: human_size_limit, human_time_limit: human_time_limit })">
    </FaqEntry>

    <FaqEntry
      id="got-error"
      :title="$t('faq.gotError')"
      :content="$t('faq.gotErrorDesc')">
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
      return `${parseInt(Constants.zimit_size_limit / 1073741824)} GiB`;
    },
    human_time_limit() {
      return `${parseInt(Constants.zimit_time_limit / 3600)} hours`;
    },
  }
}
</script>
