<script setup lang="ts">
const props = defineProps({
  id: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})
</script>

<template>
  <v-expansion-panel :key="props.id" elevation="0">
    <v-expansion-panel-title expand-icon="fa-plus" collapse-icon="fa-minus" class="expansion-title">
      {{ props.title }}
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <slot />
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<style type="text/css" scoped>
.v-expansion-panel {
  background-color: transparent;
  border-left: 0;
  border-right: 0;
  margin-bottom: 0 !important;
  border-radius: 0;
  border-top: solid lightgrey 1px;
}

.v-expansion-panel-title {
  font-size: 1rem;
  min-height: 42px;
}

.v-expansion-panel--active > .v-expansion-panel-title:not(.v-expansion-panel-title--static) {
  min-height: auto;
}

.v-expansion-panel:last-of-type {
  border-bottom: solid lightgrey 1px;
}

.v-expansion-panel-text {
  color: rgb(102, 102, 102);
}

.expansion-title :deep(.v-icon) {
  font-size: 14px;
}
</style>
