<template>
  <table
    class="table table-sm table-striped"
    :class="{ 'table-responsive': shrink }"
  >
    <tbody>
      <tr v-for="(value, name) in flags" :key="name">
        <td>{{ name }}</td>
        <td v-if="is_protected_key(name)" v-tooltip="'Actual content hidden'">
          {{ secret_replacement }}
        </td>
        <td v-else>{{ value }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script type="text/javascript">
import Constants from "../constants.js";

export default {
  name: "FlagsList",
  props: {
    flags: {
      type: Object,
      required: true,
    },
    shrink: {
      type: Boolean,
      default: () => false,
    },
    secretFields: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    secret_replacement() {
      return Constants.secret_replacement;
    },
  },
  methods: {
    is_protected_key(key) {
      return this.secretFields.indexOf(key) != -1;
    },
  },
};
</script>
