<template>
  <div class="nav-container">
    <header class="header">
      <router-link :to="{ name: 'home' }" class="logo">
        <img alt="$t('navbar.logoAlt')" src="../assets/ZIMIT_LOGO_RGB.svg">
      </router-link>
      <Loading class="loading"/>
    </header>

    <div class="language-selector-container">
      <select @change="changeLanguage($event)" class="language-selector">
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="fa">فارسی</option>
        <!-- Add more languages here -->
      </select>
    </div>
  </div>
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
    padding: .5rem 1rem;
    border-radius: .25rem;
    border: 1px solid #ced4da;
    appearance: none; 
    background-color: #fff;
    background-image: url('data:image/svg+xml;charset=UTF8,<svg ...></svg>'); /* Add a custom dropdown arrow */
    background-repeat: no-repeat;
    background-position: right .75rem center;
    background-size: 16px 12px;
  }

  [dir='rtl'] .language-selector-container {
    right: auto;
    left: 2em;
  }
</style>