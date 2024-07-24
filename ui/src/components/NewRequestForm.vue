<script setup lang="ts">
import { computed, ref, reactive, watchEffect } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMainStore } from '../stores/main';
import NewRequestSelect from './NewRequestSelect.vue';
import NewRequestSwitch from './NewRequestSwitch.vue';

const { t } = useI18n();
const mainStore = useMainStore();
const isFormValid = ref(false);
const showAdvanced = ref(false);

const hasDefinitions = computed(
  () => mainStore.offlinersDefinitions !== undefined,
);

const selectedValues = computed({
  get: () => mainStore.getFormValue(data_key),
  set: (value) => mainStore.setFormValue(data_key, value),
});

const updateSelectedValue = (
  data_key: string,
  value: string | readonly string[] | null,
) => {
  selectedValues[data_key].value = value;
};

const rules = {
  required: (value: string) => !!value || 'Required.',
  email: (value: string) => /.+@.+\..+/.test(value) || 'E-mail must be valid.',
  number: (value: string) => !isNaN(Number(value)) || 'Must be a number.',
};
</script>

<template>
  <!--<div class="container">-->

  <v-form v-if="hasDefinitions" v-model="isFormValid">
    <v-text-field
      id="zimit_url"
      :label="t('newRequest.urlLabel')"
      :value="mainStore.getFormValue('url')"
      @input="mainStore.setFormValue('url', $event.target.value)"
      type="url"
      placeholder="https://www.example.com"
      :rules="[rules.required]"
    ></v-text-field>
    <v-text-field
      id="zimit_email"
      :label="t('newRequest.emailLabel')"
      :value="mainStore.getFormValue('email')"
      @input="mainStore.setFormValue('email', $event.target.value)"
      type="email"
      placeholder="alice@example.com"
    ></v-text-field>
    <v-btn class="black" type="submit" rounded="xl" :disabled="!isFormValid">{{
      t('newRequest.submit')
    }}</v-btn>
    <v-btn flat rounded="xl" @click="showAdvanced = !showAdvanced">{{
      t('newRequest.advancedOptions')
    }}</v-btn>
    <div v-if="showAdvanced">
      {{ mainStore.formValues }}
      <table>
        <tbody>
          <tr v-for="flag in mainStore.offlinersFlags">
            <th>{{ flag.label }}</th>
            <td>
              <!-- TODO: make two way binding work with v-switch -->
              <NewRequestSwitch
                v-if="flag.type == 'boolean'"
                :data-key="flag.dataKey"
              />
              <NewRequestSelect
                v-if="
                  ['string-enum', 'list-of-string-enum'].includes(flag.type)
                "
                :choices="flag.choices"
                :multiple="flag.type == 'list-of-string-enum'"
                :data-key="flag.dataKey"
              />
              <!-- <v-select
                v-if="
                  ['string-enum', 'list-of-string-enum'].includes(flag.type)
                "
                :items="flag.choices"
                density="compact"
                :multiple="flag.type == 'list-of-string-enum'"
                :value="mainStore.getFormValue(flag.dataKey)"
                @update:model-value="
                  (value) => updateSelectedValue(flag.dataKey, value)
                "
              /> -->

              <!--<SwitchButton
                  v-if="field.component == 'switchbutton'"
                  v-model="flags[field.data_key]"
                  :name="'es_flags_' + field.data_key"
                  >{{ yes_no(flags[field.data_key], 'Enabled', 'Not set') }}
                </SwitchButton>
                <multiselect
                  v-if="field.component == 'multiselect'"
                  v-model="flags[field.data_key]"
                  :options="field.options"
                  :multiple="true"
                  :clear-on-select="true"
                  :preserve-search="true"
                  :searchable="true"
                  :close-on-select="true"
                  :placeholder="field.placeholder"
                  size="sm"
                ></multiselect>
                <component
                  :is="field.component"
                  v-if="
                    field.component != 'multiselect' &&
                    field.component != 'switchbutton'
                  "
                  v-model="flags[field.data_key]"
                  :name="'es_flags_' + field.data_key"
                  :required="field.required"
                  :placeholder="field.placeholder"
                  :style="{
                    backgroundColor: field.bind_color
                      ? flags[field.data_key]
                      : '',
                  }"
                  size="sm"
                  :step="field.step"
                  :type="field.component_type"
                >
                  <option
                    v-for="option in field.options"
                    :key="option.value"
                    :value="option.value"
                  >
                    {{ option.text }}
                  </option>
                </component>
                <b-form-text>{{ flag.description }}</b-form-text>
                -->
            </td>
          </tr>
        </tbody>
      </table>
      <v-btn
        class="black"
        type="submit"
        rounded="xl"
        :disabled="!isFormValid"
        >{{ t('newRequest.submit') }}</v-btn
      >
    </div>
  </v-form>
  <div v-else>Loading offliner definition ...</div>

  <!--


      <div v-if="showAdvanced">
        <table
          class="table table-striped table-hover table-sm table-responsive-md"
        >
          <tbody>
            <tr v-for="field in form_fields" :key="field.data_key">
              <th>
                {{ field.label
                }}<sup v-if="field.required"
                  >&nbsp;<b-icon
                    icon="asterisk"
                    font-scale=".5"
                    style="color: red"
                  ></b-icon
                ></sup>
              </th>
              <td>
                <SwitchButton
                  v-if="field.component == 'switchbutton'"
                  v-model="flags[field.data_key]"
                  :name="'es_flags_' + field.data_key"
                  >{{ yes_no(flags[field.data_key], 'Enabled', 'Not set') }}
                </SwitchButton>
                <multiselect
                  v-if="field.component == 'multiselect'"
                  v-model="flags[field.data_key]"
                  :options="field.options"
                  :multiple="true"
                  :clear-on-select="true"
                  :preserve-search="true"
                  :searchable="true"
                  :close-on-select="true"
                  :placeholder="field.placeholder"
                  size="sm"
                ></multiselect>
                <component
                  :is="field.component"
                  v-if="
                    field.component != 'multiselect' &&
                    field.component != 'switchbutton'
                  "
                  v-model="flags[field.data_key]"
                  :name="'es_flags_' + field.data_key"
                  :required="field.required"
                  :placeholder="field.placeholder"
                  :style="{
                    backgroundColor: field.bind_color
                      ? flags[field.data_key]
                      : '',
                  }"
                  size="sm"
                  :step="field.step"
                  :type="field.component_type"
                >
                  <option
                    v-for="option in field.options"
                    :key="option.value"
                    :value="option.value"
                  >
                    {{ option.text }}
                  </option>
                </component>
                <b-form-text>{{ field.description }}</b-form-text>
              </td>
            </tr>
          </tbody>
        </table>

        <b-form-group>
          <b-button
            pill
            type="submit"
            :disabled="!editorReady || !payload.url || busy"
            variant="grey"
          >
            {{ t('newRequest.submit') }}</b-button
          >
        </b-form-group>
      </div>

    </b-form>-->
</template>

<style type="text/css" scoped>
form {
  max-width: 700px;
  margin: auto;
}
/*
.form-group,
h1 {
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 1.5em;
}
  */

.v-form {
  width: 500px;
}

.v-btn {
  text-transform: none;
  background-color: transparent;
}

.v-btn.black {
  background-color: black;
  color: white;
}
</style>
