<script setup lang="ts">
import { useMainStore } from '../stores/main'

const mainStore = useMainStore()

const props = defineProps({
  dataKey: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: false,
    default: undefined
  },
  placeholder: {
    type: String,
    required: false,
    default: undefined
  },
  rules: {
    type: Array as () => Array<(value: unknown) => boolean | string>,
    required: false,
    default: undefined
  },
  description: {
    type: String,
    required: false,
    default: undefined
  }
})
</script>

<template>
  <v-textarea
    :label="props.label"
    :placeholder="props.placeholder"
    :model-value="mainStore.getFormValue(props.dataKey)"
    :hint="props.description"
    :rules="props.rules"
    hide-details="auto"
    bg-color="white"
    :persistent-hint="props.description !== undefined"
    auto-grow
    rows="3"
    @update:model-value="(value) => mainStore.setFormValue(props.dataKey, value)"
  />
</template>

<style type="text/css" scoped></style>
