<script setup lang="ts">
import { inject, computed } from 'vue'
import constants from '../constants'
import type { Config } from '../config'
import { useMainStore } from '../stores/main'

const mainStore = useMainStore()
const config = inject<Config>(constants.config)!

const props = defineProps({
  dataKey: { type: String, required: true },
  label: { type: String, default: '' },
  description: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  rules: { type: Array<Function>, default: () => [] }
})

const value = computed({
  get() {
    return mainStore.getFormValue(props.dataKey)
  },
  set(value) {
    mainStore.setFormValue(props.dataKey, value)
  }
})
</script>

<template>
  <v-textarea
    v-model="value"
    :label="label"
    :placeholder="placeholder"
    :rules="rules"
    auto-grow
    variant="outlined"
    color="black"
    density="comfortable"
    rows="5"
  >
    <template v-if="description" #details>
      <span>{{ description }}</span>
    </template>
  </v-textarea>
</template>

