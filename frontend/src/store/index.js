import { createStore } from "vuex";
import VueCookies from 'vue-cookies';

export default createStore({
  state: {
    isAuthenticated: false,
    tokens: {
      access: '',
      refresh: ''
    },
    user: {
      id: 0,
      role: '',
      email: '',
      auth_provider: '',
      full_name: '',
      image: null
    },
    notifications: []
  },
  getters: {
    getAccessToken(state) {
      return state.tokens.access
    },
    getIsAuthenticated(state) {
      return state.isAuthenticated
    },
    getUser(state) {
      return state.user
    }
  },
  mutations: {
    initializeStore(state, tokens) {
      if (tokens.access) {
        state.tokens.access = tokens.access
        state.tokens.refresh = tokens.refresh
        state.isAuthenticated = true
      } else {
        state.tokens.access = ''
        state.tokens.refresh = ''
        state.isAuthenticated = false
        localStorage.clear();
        VueCookies.remove('qab_at');
        VueCookies.remove('qab_rt');
      }
    },
    refreshToken(state, token) {
      state.tokens.access = token
    },
    setUser(state, user) {
      state.user.id = user.id
      state.user.role = user.role
      state.user.email = user.email
      state.user.auth_provider = user.auth_provider
      state.user.full_name = user.full_name
      state.user.image = user.image
    }
  },
  actions: {},
  modules: {},
});
