<script setup lang="ts">
import { useMainStore } from '../stores/main';
import constants from '../constants';

const mainStore = useMainStore();

const props = defineProps({
  dataKey: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <v-switch
    :label="
      mainStore.getFormValue(props.dataKey)
        ? 'Enabled'
        : constants.not_set_magic_value
    "
    :value="mainStore.getFormValue(props.dataKey)"
    @update:model-value="
      (value) => mainStore.setFormValue(props.dataKey, value)
    "
    inset
    color="black"
    :true-value="true"
    :false-value="undefined"
  />
</template>

<style type="text/css" scoped></style>
