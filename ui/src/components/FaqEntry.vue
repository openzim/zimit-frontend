<script setup lang="ts">
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <v-expansion-panel
    :key="props.id"
    :title="props.title"
    expand-icon="fa-plus"
    collapse-icon="fa-minus"
    elevation="0"
  >
    <template #text>
      <slot></slot>
    </template>
  </v-expansion-panel>
  <!--
  <b-card no-body class="mb-1">
    <b-card-header header-tag="header" class="p-1" role="tab">
      <b-button v-b-toggle="[id]" block variant="neutral"
        >{{ title }}
        <b-icon icon="plus" class="plus" font-scale="1.5"></b-icon>
        <b-icon icon="dash" class="minus" font-scale="1.5"></b-icon
      ></b-button>
    </b-card-header>
    <b-collapse :id="id" accordion="faq-accordion" role="tabpanel">
      <b-card-body>
        <b-card-text><slot></slot></b-card-text>
      </b-card-body>
    </b-collapse>
  </b-card>-->
</template>

<style type="text/css" scoped>
/*
.card-header .btn {
  text-align: left;
}

.card-header .plus,
.card-header .minus {
  position: absolute;
  top: 0.5em;
  right: 0.3rem;
}

:root[dir="rtl"] .card-header .plus,
:root[dir="rtl"] .card-header .minus {
  right: auto;
  left: 0.3rem;
}

.card-header .collapsed .minus {
  display: none;
}

.card-header .not-collapsed .plus {
  display: none;
}
*/
.v-expansion-panel {
  background-color: transparent;
  border-left: 0;
  border-right: 0;
  margin-bottom: 0 !important;
  border-radius: 0;
}

/*
.faq .card:not(:first-child) {
  border-top: 0;
}

.card-header {
  background-color: transparent;
  border: 0;
}
*/
</style>
