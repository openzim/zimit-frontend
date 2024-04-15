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
  <div>
    <div class="text-subtitle-2 mt-4 mb-2">Accordion</div>

    <v-expansion-panels variant="accordion">
      <v-expansion-panel
        v-for="i in 3"
        :key="i"
        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        title="Item"
      ></v-expansion-panel>
    </v-expansion-panels>
    ¨
  </div>

  <p><strong>Current route path:</strong> {{ $route.fullPath }}</p>
  <nav>
    <RouterLink to="/">Go to Home</RouterLink>
    <RouterLink to="/about">Go to About</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
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

.logo {
  width: 400px;
}
</style>
