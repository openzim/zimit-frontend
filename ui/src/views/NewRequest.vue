<script setup lang="ts">
import { computed } from 'vue';
import FaqList from '../components/FaqList.vue';
import { useI18n } from 'vue-i18n';
import { useMainStore } from '../stores/main';

const { t } = useI18n();
const mainStore = useMainStore();

const editorReady = computed(
  () => mainStore.offlinersDefinitions !== undefined,
);
</script>

<template>
  <div class="container">
    <!-- eslint-disable-next-line vue/no-v-html -->
    <h1 v-html="t('newRequest.heading')"></h1>

    <v-form v-if="editorReady"> </v-form>

    <!--
    <b-form v-if="editorReady" @submit.prevent="requestZim">
      <b-form-group>
        <b-form-input
          id="new_url"
          v-model="form.url"
          type="url"
          :placeholder="t('newRequest.urlPlaceholder')"
          required="required"
        />
      </b-form-group>

      <b-form-group>
        <b-form-input
          id="new_email"
          v-model="form.email"
          type="email"
          :placeholder="t('newRequest.emailPlaceholder')"
        />
      </b-form-group>

      <b-form-group>
        <b-button
          pill
          type="submit"
          :disabled="!editorReady || !payload.url || busy"
          variant="grey"
          >{{ t('newRequest.submit') }}</b-button
        >
        <b-button
          pill
          size="sm"
          :pressed.sync="showAdvanced"
          variant="link-grey"
          >{{ t('newRequest.advancedOptions') }}</b-button
        >
      </b-form-group>

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

      <FaqList />
    </b-form>-->
  </div>
</template>
