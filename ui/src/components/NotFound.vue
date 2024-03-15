<!-- Friendly fallback for unmatched routes -->

<template>
  <div class="container">
    <h1>{{ $t('notFound.heading') }}</h1>
    <p>{{ $t('notFound.description') }}</p>
  </div>
</template>

<script>
  export default {
    name: 'NotFound',
  }
</script>
