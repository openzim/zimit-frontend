import { defineStore } from 'pinia';

import Constants from '../constants';

export type RootState = {
  count: number;
  loading: boolean;
  loadingText: string;
  offlinersDefinitions: OfflinerDefinition | undefined;
};

export type LoadingPayload = {
  status: boolean;
  text: string;
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

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      count: 0,
      loading: false,
      loadingText: '',
      offlinersDefinitions: undefined,
    }) as RootState,
  actions: {
    setLoading(payload: LoadingPayload) {
      //toggle GUI loader
      this.loading = payload.status;
      this.loadingText = payload.text ? payload.text : '';
    },
    saveOfflinersDefinitions(offlinersDefinitions: OfflinerDefinition) {
      this.offlinersDefinitions = offlinersDefinitions;
    },
    increment() {
      this.count++;
    },
  },
  getters: {
    loadingStatus(state) {
      return { shoudDisplay: state.loading, text: state.loadingText };
    },
    offlinersFlags(state) {
      if (!state.offlinersDefinitions) {
        return [];
      }
      return state.offlinersDefinitions.flags.filter(
        (field) => Constants.zimit_fields.indexOf(field.key) > -1,
      );
    },
  },
});
