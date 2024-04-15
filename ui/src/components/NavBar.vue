<template>
  <div>
    <header>
      <router-link :to="{ name: 'home' }"
        ><img alt="Youzim.it logo" src="../assets/ZIMIT_LOGO_RGB.svg"
      /></router-link>
      <LoadingSpinner />
    </header>

    <div class="language-selector-container">
      <select class="language-selector" @change="changeLanguage($event)">
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="fa">فارسی</option>
        <!-- Add more languages here -->
      </select>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from "./LoadingSpinner.vue";

export default {
  name: "NavBar",
  components: { LoadingSpinner },
  methods: {
    changeLanguage(event) {
      this.$i18n.locale = event.target.value;
    },
  },
};
</script>

<style type="text/css" scoped="">
header {
  display: inline-flex;
  justify-content: center;
  width: 100%;
  text-align: center;
  padding-top: 2em;
  padding-bottom: 2em;
}

header img {
  max-width: 50vw;
  width: 400px;
}

.language-selector-container {
  position: absolute;
  top: 2em;
  right: 2em;
  margin-left: auto;
}

.language-selector {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: 1px solid #ced4da;
  appearance: none;
  background-color: #fff;
  background-size: 16px 12px;
}

[dir="rtl"] .language-selector-container {
  right: auto;
  left: 2em;
}
</style>
