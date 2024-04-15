import { defineStore } from 'pinia';

export type RootState = {
  count: number;
};

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      count: 0,
    }) as RootState,
  getters: {},
  actions: {
    increment() {
      this.count++;
    },
  },
});
