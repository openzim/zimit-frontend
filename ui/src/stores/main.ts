import { defineStore } from 'pinia';
import axios from 'axios';

import constants from '../constants';
import { ComposerTranslation } from 'vue-i18n';

export type RootState = {
  count: number;
  loading: boolean;
  loadingText: string;
  offlinersDefinitions: OfflinerDefinition | undefined;
  formValues: FormValue[];
};

export type LoadingPayload = {
  loading: boolean;
  text?: string;
};

export type OfflinerDefinition = {
  flags: OfflinerFlag[];
  help: string;
};

export type OfflinerFlag = {
  dataKey: string;
  description: string;
  key: string;
  label: string;
  required: boolean;
  type: string;
  choices: string[];
};

export type FormValue = {
  name: string;
  value: any;
};

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      count: 0,
      loading: false,
      loadingText: '',
      offlinersDefinitions: undefined,
      formValues: [] as FormValue[],
    }) as RootState,
  actions: {
    setLoading(payload: LoadingPayload) {
      //toggle GUI loader
      this.loading = payload.loading;
      this.loadingText = payload.text ? payload.text : '';
    },
    saveOfflinersDefinitions(offlinersDefinitions: OfflinerDefinition) {
      this.offlinersDefinitions = offlinersDefinitions;
    },
    increment() {
      this.count++;
    },
    setFormValue(name: string, value: any) {
      console.log(name + ' ' + value);
      const formValue = this.formValues.find(
        (formValue) => formValue.name === name,
      );
      if (!value || value === constants.not_set_magic_value) {
        if (formValue) {
          this.formValues.splice(this.formValues.indexOf(formValue));
        }
      } else {
        if (formValue) {
          formValue.value = value;
        } else {
          this.formValues.push({ name: name, value: value } as FormValue);
        }
      }
    },
    async loadOfflinerDefinition(t: ComposerTranslation) {
      this.setLoading({
        loading: true,
        text: t('newRequest.fetchingDefinition'),
      });
      const parent = this;
      return axios
        .get(constants.zimfarm_webapi + '/offliners/zimit')
        .then(function (response) {
          const offlinerDefinition: OfflinerDefinition = {
            flags: response.data.flags.map(
              (flag: any) =>
                ({ dataKey: flag.data_key, ...flag }) as OfflinerFlag,
            ),
            help: response.data.help,
          } as OfflinerDefinition;

          // dataKey: string;
          // description: string;
          // key: string;
          // label: string;
          // required: boolean;
          // type: string;
          // choices: string[];

          // console.log(response.data);
          // for (const flagData of response.data.flags) {
          //   offlinerDefinition.flags.push({
          //     dataKey: flagData['data_key'],
          //     key: flagData['key'],
          //   } as OfflinerFlag);
          // }
          offlinerDefinition.flags = offlinerDefinition.flags.filter(
            (flag) =>
              constants.new_request_advanced_flags.indexOf(flag.key) > -1,
          );
          console.log(offlinerDefinition);
          parent.offlinersDefinitions = offlinerDefinition;
        })
        .then(function () {
          parent.setLoading({ loading: false });
        });
    },
  },
  getters: {
    loadingStatus(state) {
      return { shoudDisplay: state.loading, text: state.loadingText };
    },
    offlinersFlags(state) {
      return state.offlinersDefinitions?.flags || [];
    },
    getFormValue: (state) => {
      return (name: string) => {
        const formValue = state.formValues.find(
          (formValue) => formValue.name === name,
        );
        if (formValue) {
          return formValue.value;
        } else {
          return undefined;
        }
      };
    },
  },
});
