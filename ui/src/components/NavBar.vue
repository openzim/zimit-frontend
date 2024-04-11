<template>
  <header class="header">
    <router-link :to="{ name: 'home' }" class="logo">
      <img alt="$t('navbar.logoAlt')" src="../assets/ZIMIT_LOGO_RGB.svg">
    </router-link>
    <Loading class="loading"/>
    
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
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 2em;
    padding-bottom: 2em;
    text-align: center;
  }

  .header .logo {
    margin: 0 auto;
  }

  .header img {
    max-width: 80%;
    width: 400px;
  }

  .language-selector {
    padding: .5rem 1rem;
    border-radius: .25rem;
    border: 1px solid #ced4da;
    appearance: none;
    background-color: #fff;
    margin-right: 1em; 
    background-image: url('data:image/svg+xml;charset=UTF8,<svg ...></svg>');
    background-repeat: no-repeat;
    background-position: right .75rem center;
    background-size: 16px 12px;
  }
  
  /* Add RTL support */
  [dir="rtl"] .language-selector {
    margin-right: 0;
    margin-left: 1em;
    background-position: left .75rem center;
  }
</style>