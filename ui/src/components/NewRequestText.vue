<script setup lang="ts">
import { useMainStore } from '../stores/main'
import constants from '../constants'
import { getRulesFromFieldType } from '../utils/utils'
import { byGrapheme } from 'split-by-grapheme'

const mainStore = useMainStore()

const getGraphemeCount = (value: unknown): number => {
  if (typeof value === 'string') {
    return value.split(byGrapheme).length
  }
  return 0
}

const truncateToMaxGraphemes = (value: string, maxLength: number): string => {
  const graphemes = value.split(byGrapheme)
  if (graphemes.length <= maxLength) {
    return value
  }
  return graphemes.slice(0, maxLength).join('')
}

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
  },
  rules: {
    type: Array as () => Array<(value: unknown) => boolean | string>,
    required: false,
    default: undefined
  },
  maxLength: {
    type: Number,
    required: false,
    default: null
  },
  description: {
    type: String,
    required: false,
    default: undefined
  }
})

const computedRules = props.rules || getRulesFromFieldType(props.type, props.required)

const handleInputWithGraphemeLimit = (value: string) => {
  const trimmedValue = value?.trim() || value

  if (props.maxLength && typeof trimmedValue === 'string') {
    const truncatedValue = truncateToMaxGraphemes(trimmedValue, props.maxLength)
    mainStore.setFormValue(props.dataKey, truncatedValue)
  } else {
    mainStore.setFormValue(props.dataKey, trimmedValue)
  }
}
</script>

<!-- Supports integer, float, url, email, text
 hex-color type is not (yet) supported
-->
<template>
  <v-text-field
    density="compact"
    :placeholder="props.placeholder"
    :label="props.label"
    :model-value="mainStore.getFormValue(props.dataKey)"
    :hint="props.description"
    :step="props.type == 'integer' ? 1 : props.type == 'float' ? 0.1 : undefined"
    :rules="computedRules"
    hide-details="auto"
    bg-color="white"
    :persistent-hint="props.description !== undefined"
    @update:model-value="handleInputWithGraphemeLimit"
  >
    <template v-if="props.maxLength" #counter>
      {{ getGraphemeCount(mainStore.getFormValue(props.dataKey)) }}/{{ props.maxLength }}
    </template>
  </v-text-field>
</template>

<style type="text/css" scoped></style>
