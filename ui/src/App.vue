<script setup lang="ts">
// import HelloWorld from './components/HelloWorld.vue';
// import FaqEntry from './components/FaqEntry.vue';
// import FaqList from './components/FaqList.vue';

import constants from './constants';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>

<template>
  <div class="text-center logo-div">
    <a :href="constants.home_page" target="_blank">
      <img
        src="./assets/ZIMIT_LOGO_RGB.svg"
        class="logo-img vue"
        alt="Vue logo"
      />
    </a>
  </div>
  <!--<NavBar />-->
  <!--<AlertFeedback />-->
  <RouterView />
  <i18n-t keypath="footer.paragraph" tag="footer" class="text-center">
    <a target="_blank" href="https://kiwix.org">{{ t('footer.link0') }}</a>
    <a target="_blank" href="https://webrecorder.net">{{
      t('footer.link1')
    }}</a>
    <a target="_blank" href="https://www.mozilla.org/moss/">{{
      t('footer.link2')
    }}</a>
  </i18n-t>
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

/* RTL styles */
[dir='rtl'] #app {
  direction: rtl;
  text-align: right;
}

[dir='rtl'] footer {
  direction: rtl;
}

.logo-img {
  width: 400px;
}

.logo-div {
  padding-top: 2em;
  padding-bottom: 2em;
}
</style>
