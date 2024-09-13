<script setup lang="ts">
import { useMainStore } from '../stores/main'
import constants from '../constants'
import { getRulesFromFieldType } from '../utils/utils'

const mainStore = useMainStore()

const props = defineProps({
  dataKey: {
    type: String,
    required: true
  },
  type: {
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
    default: constants.not_set_magic_value
  },
  required: {
    type: Boolean,
    default: false
  }
})
</script>

<!-- Supports integer, float, url, email, text
 hex-color type is not (yet) supported
-->
<template>
  <v-text-field
    density="compact"
    :placeholder="props.placeholder"
    :label="props.label"
    :value="mainStore.getFormValue(props.dataKey)"
    :step="props.type == 'integer' ? 1 : props.type == 'float' ? 0.1 : undefined"
    :rules="getRulesFromFieldType(props.type, props.required)"
    hide-details="auto"
    bg-color="white"
    @update:model-value="(value) => mainStore.setFormValue(props.dataKey, value)"
  />
</template>

<style type="text/css" scoped></style>
