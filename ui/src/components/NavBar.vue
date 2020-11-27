<template>
    <header>
        <nav class="navbar navbar-expand-md navbar-dark">
            <a class="navbar-brand branding">
                <div class="icon"><img alt="Kiwix logo" src="../assets/Kiwix_logo_v3.svg">
                <Loading/>
                </div>
                <label>Zimit</label>
            </a>
        </nav>
    </header>
</template>

<script>
  import Loading from './Loading.vue'
  // import ZimfarmMixins from './Mixins.js'

  export default {
    name: 'NavBar',
    // mixins: [ZimfarmMixins],
    components: {Loading},
  }
</script>
