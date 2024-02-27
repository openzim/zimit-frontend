<template>
  <div class="container">
    <h1>Want an offline version of a website? Just <strong>Zim it</strong>!</h1>

    <b-form @submit.prevent="requestZim" v-if="editorReady">
        <b-form-group>
            <b-form-input
                type="url"
                id="new_url"
                placeholder="Full URL of the website to convert"
                required="required"
                v-model="form.url" />
        </b-form-group>

        <b-form-group>
            <b-form-input
                type="email"
                id="new_email"
                placeholder="Your e-mail to receive a download link. Address not kept"
                v-model="form.email" />
        </b-form-group>


        <b-form-group>
          <b-button
            pill
            type="submit"
            :disabled="!editorReady || !payload.url || busy"
            variant="grey">
            Let's Zim it!</b-button>
          <b-button
            pill
            size="sm"
            :pressed.sync="showAdvanced"
            variant="link-grey">advanced options</b-button>
        </b-form-group>

        <div v-if="showAdvanced">
            <table class="table table-striped table-hover table-sm table-responsive-md">
            <tbody>
            <tr v-for="field in form_fields" :key="field.data_key">
            <th>{{ field.label }}<sup v-if="field.required">&nbsp;<b-icon icon="asterisk" font-scale=".5" style="color: red;"></b-icon></sup></th>
            <td>
               <SwitchButton
                    v-if="field.component == 'switchbutton'"
                    :name="'es_flags_' + field.data_key"
                    v-model="flags[field.data_key]">{{ flags[field.data_key]|yes_no("Enabled", "Not set") }}
                </SwitchButton>
              <multiselect v-if="field.component == 'multiselect'"
                v-model="flags[field.data_key]"
                :options="field.options"
                :multiple="true"
                :clear-on-select="true"
                :preserve-search="true"
                :searchable="true"
                :closeOnSelect="true"
                :placeholder="field.placeholder"
                size="sm"></multiselect>
              <component v-if="field.component != 'multiselect' && field.component != 'switchbutton'"
                :is="field.component"
                :name="'es_flags_' + field.data_key"
                :required="field.required"
                :placeholder="field.placeholder"
                v-model="flags[field.data_key]"
                :style="{backgroundColor: field.bind_color ? flags[field.data_key]: ''}"
                size="sm"
                :step="field.step"
                :type="field.component_type">
                  <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.text }}</option>
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
                variant="grey">
                Let's Zim it!</b-button>
            </b-form-group>

        </div>

        <Faq />


    </b-form>
  </div>
</template>

<script>
    import Constants from '../constants.js'
    import Mixins from '../components/mixins.js'
    import SwitchButton from '../components/SwitchButton.vue'
    import Faq from '../components/Faq.vue'

    export default {
      name: 'NewRequest',
      mixins: [Mixins],
      components: {SwitchButton, Faq},
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
            return this.form && this.offliner_def !== null; },
        form_fields() {
            let fields = [];
            for (var i=0;i<this.offliner_def.length;i++) {
              let field = this.offliner_def[i];
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
                step = 0.1
              }

              if (field.type == "list-of-string-enum") {
                component = "multiselect";
                options = field.choices;
              }

              if (field.type == "boolean") {
                component = "switchbutton";
                options = [{text: "True", value: true}, {text: "Not set", value: undefined}];
              }

              if (field.type == "string-enum") {
                component = "b-form-select";
                options = field.choices.map(function (option) { return {text: option, value: option}; });
                if (field.required != true) {
                  options.push({text: "Not set", value: undefined});
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
                placeholder: "Not set",  //field.placeholder,

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
            return {url: this.form.url, email:this.form.email, flags: this.flags};
          }
      },
      methods: {
        loadRecipeDefinition(force_reload, on_success, on_error) {
            if (!force_reload && this.$store.getters.offliner_def.length){
                if (on_success) { on_success(); }
                return;
            }

            let parent = this;
            console.debug("fetching definition…");
            parent.toggleLoader("fetching definition…");
            parent.queryAPI('get', Constants.zimfarm_webapi + '/offliners/zimit')
              .then(function (response) {
                  let definition = response.data.filter(field => Constants.zimit_fields.indexOf(field.key) > -1);
                  parent.$store.dispatch('setOfflinerDef', definition);

                  if (on_success) { on_success(); }
              })
              .catch(function (error) {
                if (on_error) { on_error(Constants.standardHTTPError(error.response)); }
              })
              .then(function () {
                  parent.toggleLoader(false);
              });
        },
        requestZim() {
            console.log("requestZim");

            let parent = this;
            this.payload.flags = Object.filter(this.payload.flags, item => item!==""); 
            parent.busy = true;
            let task_id = null;
            parent.toggleLoader("Creating schedule…");
            parent.queryAPI('post', Constants.zimitui_api + '/requests/', this.payload)
              .then(function (response) {
                if (response.data && response.data.id) {
                  task_id = response.data.id;
                  parent.redirectTo('request', {task_id: task_id});
                } else
                  throw "Didn't receive task_id";
              })
              .catch(function (error) {
                parent.alertError("Unable to request ZIM creation:<br />" + Constants.standardHTTPError(error.response));
              })
              .then(function () {
                parent.toggleLoader(false);
                parent.busy = false;
              });
        },
      },
      mounted() {
        this.loadRecipeDefinition(false);
    },
    }
</script>

<style type="text/css" scoped>
  h1 {
    text-align: center;
  }

  form {
    max-width: 700px;
    margin: auto;
  }

  .form-group, h1 {
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
