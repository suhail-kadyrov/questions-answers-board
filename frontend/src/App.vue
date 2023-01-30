<template>
  <v-app>
    <v-main>
      <v-content>
        <router-view />
      </v-content>
    </v-main>
  </v-app>
</template>

<script setup>
import axios from "axios";
import { onMounted, inject } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
const $cookies = inject("$cookies");
const store = useStore();
const router = useRouter();

onMounted(async () => {
  store.commit("initializeStore", {
    access: $cookies.get("qab_at"),
    refresh: $cookies.get("qab_rt"),
  });
  if (store.getters.getAccessToken) {
    axios.defaults.headers.common["Authorization"] =
      "Bearer " + store.getters.getAccessToken;
    await axios
      .get("/profile/")
      .then((response) => {
        store.commit("setUser", response.data);
      })
      .catch((error) => {
        error;
        store.commit("initializeStore", {});
        router.push({ name: 'login' })
      });
  } else {
    axios.defaults.headers.common["Authorization"] = "";
  }
});
</script>

<style lang="scss">
html {
  overflow-y: auto !important;
}

body {
  font-family: "Arial", sans-serif !important;
}

.auth- {
  &btns {
    text-transform: none !important;
  }
  &links {
    letter-spacing: .05rem;
    &:hover {
      text-decoration: underline !important;
    }
  }
}

.medium-text {
  font-size: 1.3rem !important;
  line-height: 1.3rem;
  input,
  .v-label {
    font-size: 1.2rem;
  }
}
</style>
