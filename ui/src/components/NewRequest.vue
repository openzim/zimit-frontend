<template>
  <div class="container">
    <!-- eslint-disable-next-line vue/no-v-html -->
    <h1 v-html="$t('newRequest.heading')"></h1>

    <b-form v-if="editorReady" @submit.prevent="requestZim">
      <b-form-group>
        <b-form-input
          id="new_url"
          v-model="form.url"
          type="url"
          :placeholder="$t('newRequest.urlPlaceholder')"
          required="required"
        />
      </b-form-group>

      <b-form-group>
        <b-form-input
          id="new_email"
          v-model="form.email"
          type="email"
          :placeholder="$t('newRequest.emailPlaceholder')"
        />
      </b-form-group>

      <b-form-group>
        <b-button
          pill
          type="submit"
          :disabled="!editorReady || !payload.url || busy"
          variant="grey"
          >{{ $t("newRequest.submit") }}</b-button
        >
        <b-button
          v-model:pressed="showAdvanced"
          pill
          size="sm"
          variant="link-grey"
          >{{ $t("newRequest.advancedOptions") }}</b-button
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
                  >{{ yes_no(flags[field.data_key], "Enabled", "Not set") }}
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
            {{ $t("newRequest.submit") }}</b-button
          >
        </b-form-group>
      </div>

      <FaqList />
    </b-form>
  </div>
</template>

<script>
import Constants from "../constants.js";
import Mixins from "../components/mixins.js";
import SwitchButton from "../components/SwitchButton.vue";
import FaqList from "../components/FaqList.vue";

export default {
  name: "NewRequest",
  components: { SwitchButton, Faq },
  mixins: [Mixins],
  data() {
    return {
      form: {},
      flags: {},
      showAdvanced: false,
      busy: false, // whether a request is currently being sent
    };
  },
  computed: {
    editorReady() {
      return this.form && this.offliner_def !== null;
    },
    form_fields() {
      const fields = [];
      for (var i = 0; i < this.offliner_def.length; i++) {
        const field = this.offliner_def[i];
        let component = "b-form-input";
        let options = null;
        let component_type = null;
        let bind_color = null;
        let step = null;

        if (field.type == "hex-color") {
          bind_color = true;
        }

        if (field.type == "url") {
          component = "b-form-input";
          component_type = "url";
        }

        if (field.type == "email") {
          component = "b-form-input";
          component_type = "email";
        }

        if (field.type == "integer") {
          component = "b-form-input";
          component_type = "number";
          step = 1;
        }

        if (field.type == "float") {
          component = "b-form-input";
          component_type = "number";
          step = 0.1;
        }

        if (field.type == "list-of-string-enum") {
          component = "multiselect";
          options = field.choices;
        }

        if (field.type == "boolean") {
          component = "switchbutton";
          options = [
            { text: this.$t("newRequest.true"), value: true },
            { text: this.$t("newRequest.notSet"), value: undefined },
          ];
        }

        if (field.type == "string-enum") {
          component = "b-form-select";
          options = field.choices.map((option) => ({
            text: option,
            value: option,
          }));
          if (field.required != true) {
            options.push({
              text: this.$t("newRequest.notSet"),
              value: undefined,
            });
          }
        }

        if (field.type == "text") {
          component = "b-form-input";
          component_type = "text";
        }

        fields.push({
          label: field.label || field.data_key,
          data_key: field.data_key,
          required: field.required,
          description: field.description,
          placeholder: this.$t("newRequest.notSet"), //field.placeholder,

          component: component,
          component_type: component_type,
          options: options,
          bind_color: bind_color,
          step: step,
        });
      }
      return fields;
    },
    payload() {
      return { url: this.form.url, email: this.form.email, flags: this.flags };
    },
  },
  mounted() {
    this.loadRecipeDefinition(false);
  },
  methods: {
    yes_no(value, value_yes, value_no) {
      if (!value_yes) value_yes = "yes";
      if (!value_no) value_no = "no";
      return value ? value_yes : value_no;
    },
    loadRecipeDefinition(force_reload, on_success, on_error) {
      if (!force_reload && this.$store.getters.offliner_def.length) {
        if (on_success) {
          on_success();
        }
        return;
      }

      const parent = this;
      console.debug("fetching definition…");
      parent.toggleLoader(this.$t("newRequest.fetchingDefinition"));
      parent
        .queryAPI("get", Constants.zimfarm_webapi + "/offliners/zimit")
        .then(function (response) {
          const definition = response.data.filter(
            (field) => Constants.zimit_fields.indexOf(field.key) > -1,
          );
          parent.$store.dispatch("setOfflinerDef", definition);

          if (on_success) {
            on_success();
          }
        })
        .catch(function (error) {
          if (on_error) {
            on_error(
              parent.$t("newRequest.standardHTTPError", {
                error: Constants.standardHTTPError(error.response),
              }),
            );
          }
        })
        .then(function () {
          parent.toggleLoader(false);
        });
    },
    requestZim() {
      console.log("requestZim");

      const parent = this;
      this.payload.flags = Object.filter(
        this.payload.flags,
        (item) => item !== "",
      );
      parent.busy = true;
      let task_id = null;
      parent.toggleLoader(this.$t("newRequest.creatingSchedule"));
      parent
        .queryAPI("post", Constants.zimitui_api + "/requests/", this.payload)
        .then(function (response) {
          if (response.data && response.data.id) {
            task_id = response.data.id;
            parent.redirectTo("request", { task_id: task_id });
          } else throw new Error(parent.$t("newRequest.noTaskIdReceived"));
        })
        .catch(function (error) {
          parent.alertError(
            parent.$t("newRequest.unableToRequestZIM", {
              error: Constants.standardHTTPError(error.response),
            }),
          );
        })
        .then(function () {
          parent.toggleLoader(false);
          parent.busy = false;
        });
    },
  },
};
</script>

<style type="text/css" scoped>
h1 {
  text-align: center;
}

form {
  max-width: 700px;
  margin: auto;
}

.form-group,
h1 {
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 1.5em;
}

.faq {
  margin-top: 5rem;
  margin-bottom: 3rem;
}
</style>
