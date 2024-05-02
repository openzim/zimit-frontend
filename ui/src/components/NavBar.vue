<template>
    <header>
      <router-link :to="{ name: 'home' }"><img alt="Zimit logo" src="../assets/ZIMIT_LOGO_RGB.svg"></router-link>
      <Loading/>
    </header>
</template>

<script>
  import Loading from './Loading.vue'

  export default {
    name: 'NavBar',
    components: {Loading},
  }
</script>

<style type="text/css" scoped="">
  header {
    text-align: center;
    padding-top: 2em;
    padding-bottom: 2em;
  }
  header img { max-width: 80%; width: 400px; }
</style>
