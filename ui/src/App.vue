<template>
  <div id="app">
    <NavBar />
    <div class="container">
      <AlertFeedback />
      <router-view />
    </div>
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

<style>

</style>
