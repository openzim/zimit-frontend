<script setup lang="ts">
import { computed, inject, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { byGrapheme } from 'split-by-grapheme'
import type { Config } from '../config'
import constants from '../constants'
import { useMainStore, type OfflinerFlag } from '../stores/main'
import NewRequestSelect from './NewRequestSelect.vue'
import NewRequestSwitch from './NewRequestSwitch.vue'
import NewRequestText from './NewRequestText.vue'

const { t } = useI18n()
const mainStore = useMainStore()
const config = inject<Config>(constants.config)!
const isFormValid = ref(false)
const showAdvanced = ref(false)

const offlinerFlags = computed(
  () =>
    mainStore.offlinerDefinition?.flags.filter(
      (flag) => config.new_request_advanced_flags.indexOf(flag.data_key) > -1
    ) || []
)

const getFlagRules = (flag: OfflinerFlag) => {
  const rules: Array<(value: unknown) => boolean | string> = []

  if (flag.required) {
    rules.push((value: unknown) => {
      if (!value || value === '' || value === undefined || value === null) {
        return 'This field is required'
      }
      return true
    })
  }

  // Add type-specific validation
  if (flag.type === 'url') {
    rules.push((value: unknown) => {
      if (value && typeof value === 'string' && value !== '') {
        try {
          new URL(value)
          return true
        } catch {
          return 'Please enter a valid URL'
        }
      }
      return true
    })
  }

  if (flag.type === 'email') {
    rules.push((value: unknown) => {
      if (value && typeof value === 'string' && value !== '') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value)) {
          return 'Please enter a valid email address'
        }
      }
      return true
    })
  }

  if (flag.type === 'integer' || flag.type === 'float') {
    rules.push((value: unknown) => {
      if (value && value !== '') {
        const num = Number(value)
        if (isNaN(num)) {
          return 'Please enter a valid number'
        }
      }
      return true
    })
  }

  // Add validation for min, max, min_length, and pattern constraints
  const shouldValidate = (value: unknown) => {
    return value !== null && value !== undefined && value !== ''
  }

  // Min length validation
  if (flag.min_length !== null) {
    rules.push((value: unknown) => {
      if (shouldValidate(value) && typeof value === 'string') {
        if (value.split(byGrapheme).length < flag.min_length!) {
          return `Minimum length is ${flag.min_length} characters`
        }
      }
      return true
    })
  }

  // Max length validation
  if (flag.max_length !== null) {
    rules.push((value: unknown) => {
      if (shouldValidate(value) && typeof value === 'string') {
        if (value.split(byGrapheme).length > flag.max_length!) {
          return `Maximum length is ${flag.max_length} characters`
        }
      }
      return true
    })
  }

  // Min value validation (for numbers)
  if (flag.min !== null) {
    rules.push((value: unknown) => {
      if (shouldValidate(value)) {
        const num = Number(value)
        if (!isNaN(num) && num < flag.min!) {
          return `Minimum value is ${flag.min}`
        }
      }
      return true
    })
  }

  // Max value validation (for numbers)
  if (flag.max !== null) {
    rules.push((value: unknown) => {
      if (shouldValidate(value)) {
        const num = Number(value)
        if (!isNaN(num) && num > flag.max!) {
          return `Maximum value is ${flag.max}`
        }
      }
      return true
    })
  }

  // Pattern validation (regex)
  if (flag.pattern !== null) {
    rules.push((value: unknown) => {
      if (shouldValidate(value) && typeof value === 'string') {
        try {
          // construct the regex from the pattern string
          const regex = new RegExp(flag.pattern!)
          if (!regex.test(value)) {
            return `Value must match pattern: ${flag.pattern}`
          }
        } catch {
          // If regex is invalid, skip validation
          console.warn(`Invalid regex pattern for field ${flag.data_key}:`, flag.pattern)
        }
      }
      return true
    })
  }

  return rules
}

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
            v-for="(flag, index) in offlinerFlags"
            :key="flag.key"
            :class="{ 'striped-row': index % 2 === 0 }"
          >
            <th>{{ flag.label }}</th>
            <td>
              <NewRequestSwitch v-if="flag.type == 'boolean'" :data-key="flag.data_key" />
              <NewRequestSelect
                v-else-if="
                  ['string-enum', 'list-of-string-enum'].includes(flag.type) && flag.choices
                "
                :choices="flag.choices"
                :multiple="flag.type == 'list-of-string-enum'"
                :data-key="flag.data_key"
              />
              <NewRequestText
                v-else
                :data-key="flag.data_key"
                :type="flag.type"
                :rules="getFlagRules(flag)"
              />
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
