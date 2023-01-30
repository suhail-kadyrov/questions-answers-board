import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueCookies from 'vue-cookies'
import { loadFonts } from "./plugins/webfontloader";
import vue3GoogleLogin from 'vue3-google-login'
import axios from 'axios'

loadFonts();

axios.defaults.baseURL = 'https://q-a-board-api.herokuapp.com/api/v1'

axios.interceptors.request.use(async request => {
    const shouldRefreshAt = localStorage.getItem('shouldRefreshAt');
    const refreshToken = VueCookies.get('qab_rt');
    const shouldRefresh = shouldRefreshAt && refreshToken && (+shouldRefreshAt < Date.now());

    if (shouldRefresh) {
        localStorage.removeItem('shouldRefreshAt');
        await axios.post('/auth/refresh/', { refresh: refreshToken })
            .then(response => {
                VueCookies.set("qab_at", response.data.access, localStorage.getItem('rememberMe') ? "7d" : "", "", "", true);
                localStorage.setItem("shouldRefreshAt", new Date().getTime() + 55 * 60 * 1000);
                store.commit('refreshToken', response.data.access);
                axios.defaults.headers.common['Authorization'] = "Bearer " + response.data.access;
                request.headers.Authorization = `Bearer ${response.data.access}`;
                return request
            })
            .catch(error => {
                console.log(error);
                return request
            });
    }
    return request
});

const gAuthClientId = '555841857687-r788j6ini0mo4tivjbfgtk8p0k1pctds.apps.googleusercontent.com';

createApp(App).use(router).use(store).use(vuetify).use(vue3GoogleLogin, { clientId: gAuthClientId }).use(VueCookies, { expires: '7d'}).mount("#app");
