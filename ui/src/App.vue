<template>
  <div id="app">
    <NavBar />
      <AlertFeedback />
      <router-view />
    <footer>
      Powered By <a target="_blank" href="https://kiwix.org">Kiwix</a> <b-icon icon="heart-fill" style="color: rgb(234, 74, 170);"></b-icon>
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

<style scoped>
#app {
  margin-bottom: 4em;
}
footer {
  height: 4em;
  background-color: white;
  width: 100%;
  position: fixed;
  bottom: 0;
  text-align: center;
  padding-top: 1em;
  padding-bottom: 1em;
}
</style>
