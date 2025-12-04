<script setup lang="ts">
import { useMainStore } from '../stores/main'
import constants from '../constants'

const mainStore = useMainStore()

const props = defineProps({
  choices: {
    type: Array<{ title: string; value: string | undefined }>,
    required: true
  },
  multiple: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  dataKey: {
    type: String,
    required: true
  }
})
</script>

<template>
  <v-select
    :items="props.choices"
    density="compact"
    :multiple="props.multiple"
    :model-value="mainStore.getFormValue(dataKey)"
    hide-details="auto"
    bg-color="white"
    :placeholder="constants.not_set_magic_value"
    @update:model-value="(value) => mainStore.setFormValue(props.dataKey, value)"
  />
</template>

<style type="text/css" scoped></style>
