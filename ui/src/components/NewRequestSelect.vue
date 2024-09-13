<script setup lang="ts">
import { computed } from 'vue'
import { useMainStore } from '../stores/main'
import constants from '../constants'

const mainStore = useMainStore()

const props = defineProps({
  choices: {
    type: Array<string>,
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
const choices = computed(() => {
  return [...props.choices, constants.not_set_magic_value]
})
</script>

<template>
  <v-select
    :items="choices"
    density="compact"
    :multiple="props.multiple"
    :value="mainStore.getFormValue(dataKey) || constants.not_set_magic_value"
    hide-details="auto"
    bg-color="white"
    @update:model-value="(value) => mainStore.setFormValue(props.dataKey, value)"
  />
</template>

<style type="text/css" scoped></style>
