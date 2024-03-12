<template>
  <header>
    <router-link :to="{ name: 'home' }"><img alt="$t('navbar.logoAlt')" src="../assets/ZIMIT_LOGO_RGB.svg"></router-link>
    <Loading/>

    <!-- Language Dropdown -->
    <select @change="changeLanguage($event)" class="language-selector">
      <option value="en">English</option>
      <option value="fr">Français</option>
      <option value="fa">فارسی</option>
      <!-- Add more languages here -->
    </select>
  </header>
</template>

<script>
import Loading from './Loading.vue'

export default {
  name: 'NavBar',
  components: {Loading},
  methods: {
    changeLanguage(event) {
      this.$i18n.locale = event.target.value;
    }
  }
}
</script>

<style type="text/css" scoped="">
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

header img {
  max-width: 80%;
  width: 400px;
}

.language-selector {
  padding: .5rem 1rem;
  border-radius: .25rem;
  border: 1px solid #ced4da;
  appearance: none; /* Remove default styling */
  background-color: #fff;
  background-image: url('data:image/svg+xml;charset=UTF8,<svg ...></svg>'); /* Add a custom dropdown arrow */
  background-repeat: no-repeat;
  background-position: right .75rem center;
  background-size: 16px 12px;
}
</style>
