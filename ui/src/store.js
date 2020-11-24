
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loading: false,
    loading_text: "",

    offliner_def: [],
  },
  mutations: {
    setLoading (state, payload) { // toggle GUI loader
      state.loading = payload.status;
      state.loading_text = payload.text ? payload.text : "";
    },
    saveOfflinerDef(state, payload) {
      state.offliner_def = payload;
    },
  },
  actions: {
    setLoading(context, payload) {
      context.commit('setLoading', payload);
    },
    setOfflinerDef(context, payload) {
      context.commit('saveOfflinerDef', payload);
    },
  },
  getters: {
    loadingStatus(state) { return {should_display: state.loading, text: state.loading_text};},
    offliner_def(state) { return state.offliner_def; },
  }
})

export default store;
