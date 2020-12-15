<template>
  <div id="app">
    <NavBar />
    <AlertFeedback />
    <router-view />
    <footer>
      Powered by <a target="_blank" href="https://kiwix.org">Kiwix</a> and <a target="_blank" href="https://webrecorder.net">Webrecorder</a>, thanks to a <a target="_blank" href="https://www.mozilla.org/moss/">Mozilla Open-Source Support</a> Award <b-icon icon="heart-fill" style="color: rgb(234, 74, 170);" />
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
</style>
