<template>
  <div class="faq" role="tablist">
    <FaqEntry
      id="what-is-zim"
      title="What is a ZIM file?">
      The ZIM file format stores website content for <a target="_blank" href="https://en.wikipedia.org/wiki/Offline">offline</a> usage. It assembles the normal constituent of a website into a single archive, and compresses it so as to make it easier to save, share, and store.
    </FaqEntry>

    <FaqEntry
      id="how-to-read"
      title="How do I read my ZIM files?">
      You will need a ZIM file reader. This usually means <a target="_blank" href="https://kiwix.org/">Kiwix</a>, which is available on <a target="_blank" href="https://kiwix.org/en/applications/">desktop computers, mobile devices, and more</a>.
    </FaqEntry>

    <FaqEntry
      id="missing-content"
      title="The ZIM file is incomplete or smaller than the original website">
      Because of the very nature of this tool, we can’t leave it open for unlimited requests towards any website. That could be harmful both for our infrastructure, but also for the target websites. We currently enforce two limits: {{ human_size_limit }} file size and {{ human_time_limit }}.
    </FaqEntry>

    <FaqEntry
      id="got-error"
      title="I got an error message (no zim) or could not read a zim file">
      Triple-check the URL you entered, and if it is still not working then open a bug ticket on <a target="_blank" href="https://github.com/openzim/zimit/issues">github</a>. Indicate the target website, the request number (it’s in the email you received), and the device you tried to open your zim file on.
    </FaqEntry>
  </div>
</template>

<script type="text/javascript">
  import FaqEntry from './FaqEntry.vue'
  import Constants from '../constants.js'

  export default {
    name: 'Faq',
    components: {FaqEntry},
    computed: {
        human_size_limit() { return `${parseInt(Constants.zimit_size_limit / 1073741824)} GiB`; },
        human_time_limit() { return `${parseInt(Constants.zimit_time_limit / 3600)} hours`; },
    }
  }
</script>
