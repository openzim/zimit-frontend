<template>
    <header>
      <router-link :to="{ name: 'home' }"><img alt="Youzim.it logo" src="../assets/Youzimit-logo.png"></router-link>
      <Loading/>
      <router-link :to="{ name: 'faq' }">
        <b-icon
          icon="info-circle"
          variant="primary"
          font-scale="2.5"
          v-b-tooltip.hover
          title="FAQ"></b-icon></router-link>
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
  header .b-icon {
    position: absolute;
    right: 5%;
  }
</style>
