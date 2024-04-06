<template>
  <div id="app">
    <NavBar />
    <AlertFeedback />
    <router-view />
    <footer>
      {{ $t('app.poweredBy') }} 
      <a target="_blank" :href="$t('app.kiwixLink')">{{ $t('app.kiwix') }}</a>
      {{ $t('app.and') }} 
      <a target="_blank" :href="$t('app.webrecorderLink')">{{ $t('app.webrecorder') }}</a>, 
      <span v-html="$t('app.thanksToMozilla')"></span>
      <b-icon icon="heart-fill" style="color: rgb(234, 74, 170);" />
    </footer>
  </div>
</template>

<script>
    import NavBar from './components/NavBar.vue'
    import AlertFeedback from './components/AlertFeedback.vue'

    export default {
      name: 'app',
      components: {NavBar, AlertFeedback},
    };
</script>

<style type="text/css" scoped>
#app {
  margin-bottom: 6em;
}
footer {
  background-color: white;
  width: 100%;
  position: fixed;
  bottom: 0;
  text-align: center;
  padding-top: 1em;
  padding-bottom: 1em;
}

/* RTL styles */
[dir="rtl"] #app {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] footer {
  direction: rtl;
  text-align: center; /* Keep footer text centered or change as needed */
}
</style>
