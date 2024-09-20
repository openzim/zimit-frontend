<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useMainStore } from '../stores/main'
import NewRequestSelect from './NewRequestSelect.vue'
import NewRequestSwitch from './NewRequestSwitch.vue'
import NewRequestText from './NewRequestText.vue'

const { t } = useI18n()
const mainStore = useMainStore()
const isFormValid = ref(false)
const showAdvanced = ref(false)

const hasDefinitions = computed(() => mainStore.offlinerDefinition !== undefined)
</script>

<template>
  <v-form v-if="hasDefinitions" v-model="isFormValid">
    <v-container class="small-width">
      <NewRequestText
        data-key="url"
        type="url"
        :label="t('newRequest.urlLabel')"
        placeholder="https://www.example.com"
        :required="true"
      />
      <NewRequestText
        class="pt-4"
        data-key="email"
        type="email"
        :label="t('newRequest.emailLabel')"
        placeholder="alice@example.com"
      />
      <div class="pt-4 pb-4">
        <v-btn
          class="black"
          rounded="xl"
          :disabled="!isFormValid"
          @click="mainStore.submitRequest()"
          >{{ t('newRequest.submit') }}</v-btn
        >
        <v-btn flat rounded="xl" @click="showAdvanced = !showAdvanced">{{
          t('newRequest.advancedOptions')
        }}</v-btn>
      </div>
    </v-container>
    <div :class="{ hidden: !showAdvanced }">
      <v-table id="advanced-settings">
        <tbody>
          <tr
            v-for="(flag, index) in mainStore.offlinerFlags"
            :key="flag.key"
            :class="{ 'striped-row': index % 2 === 0 }"
          >
            <th>{{ flag.label }}</th>
            <td>
              <NewRequestSwitch v-if="flag.type == 'boolean'" :data-key="flag.data_key" />
              <NewRequestSelect
                v-else-if="['string-enum', 'list-of-string-enum'].includes(flag.type)"
                :choices="flag.choices"
                :multiple="flag.type == 'list-of-string-enum'"
                :data-key="flag.data_key"
              />
              <NewRequestText v-else :data-key="flag.data_key" :type="flag.type" />
              <span>{{ flag.description }}</span>
            </td>
          </tr>
        </tbody>
      </v-table>
      <v-container class="small-width">
        <v-btn
          class="black"
          rounded="xl"
          :disabled="!isFormValid"
          @click="mainStore.submitRequest()"
          >{{ t('newRequest.submit') }}</v-btn
        >
      </v-container>
    </div>
  </v-form>
</template>

<style type="text/css" scoped>
form {
  max-width: 700px;
  margin: auto;
}

.v-btn {
  text-transform: none;
  background-color: transparent;
}

.v-btn.black {
  background-color: black;
  color: white;
}

#advanced-settings {
  width: 100%;
}

#advanced-settings th {
  width: 20%;
}

#advanced-settings td {
  padding: 10px;
}

#advanced-settings span {
  font-size: 12px;
}

.striped-row {
  background-color: #f0f0f0;
}

.small-width {
  max-width: 500px;
}

.hidden {
  display: none;
}
</style>
