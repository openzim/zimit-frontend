<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue';
</script>

<template>
  <div>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/ZIMIT_LOGO_RGB.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Are you Vite + Vue" />
</template>

<style scoped>
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
[dir='rtl'] #app {
  direction: rtl;
  text-align: right;
}

[dir='rtl'] footer {
  direction: rtl;
  text-align: center; /* Keep footer text centered or change as needed */
}
</style>
