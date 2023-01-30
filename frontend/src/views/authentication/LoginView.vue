<template>
  <AuthBoard>
    <template v-slot:page-name> Log in </template>
    <template v-slot:default>
      <v-alert v-if="errors.length" type="error" class="mb-4 medium-text">
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </v-alert>
      <v-text-field
        v-model="email"
        clearable
        label="Email"
        prepend-inner-icon="mdi-email"
        placeholder="name@example.com"
        type="email"
        variant="outlined"
        class="medium-text"
        @keyup="submitForm($event)"
      ></v-text-field>
      <v-text-field
        v-model="password"
        label="Password"
        prepend-inner-icon="mdi-lock"
        :append-inner-icon="!showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        variant="outlined"
        class="medium-text"
        hide-details
        @keyup="submitForm($event)"
        @click:append-inner="showPassword = !showPassword"
      ></v-text-field>
      <v-checkbox
        v-model="rememberMe"
        label="Remember me"
        color="secondary"
        class="medium-text"
        hide-details
      ></v-checkbox>
    </template>
    <template v-slot:actions>
      <div class="w-100 d-flex justify-space-evenly mb-4 px-4">
        <v-btn
          variant="tonal"
          color="secondary"
          :loading="isLoading"
          :disabled="isLoading"
          :block="true"
          class="medium-text auth-btns"
          @click="login('email')"
        >
          Log in
        </v-btn>
      </div>
      <div class="my-4">
        <GoogleLogin :callback="callback" />
      </div>
      <div class="w-100 d-flex justify-space-evenly">
        <router-link
          :to="{ name: 'signup' }"
          class="text-secondary text-decoration-none auth-links"
          >Create account</router-link
        >
        <router-link
          :to="{ name: 'reset-password' }"
          class="text-secondary text-decoration-none auth-links"
          >Forgot password?</router-link
        >
      </div>
    </template>
  </AuthBoard>
</template>

<script setup>
import AuthBoard from "@/components/AuthBoard.vue";
import axios from "axios";
import { ref, reactive, inject } from "vue";
import { useStore } from "vuex";
const store = useStore();
const $cookies = inject("$cookies");
const errors = reactive([]);
const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const showPassword = ref(false);
const isLoading = ref(false);

async function login(provider, credential) {
  isLoading.value = true;
  errors.length = 0;
  axios.defaults.headers.common["Authorization"] = "";
  $cookies.remove("qab_at");
  $cookies.remove("qab_rt");
  store.commit("initializeStore", {});
  localStorage.clear();
  const formData =
    provider === "email"
      ? {
          email: email.value,
          password: password.value,
        }
      : { id_token: credential };
  const path = provider === "email" ? "/auth/login/" : "/auth/google/";
  await axios
    .post(path, formData)
    .then((response) => {
      store.commit("initializeStore", response.data.tokens);
      store.commit("setUser", response.data);
      axios.defaults.headers.common["Authorization"] =
        "Bearer " + response.data.tokens.access;
      $cookies.set(
        "qab_at",
        response.data.tokens.access,
        rememberMe.value ? "7d" : "",
        "",
        "",
        true
      );
      $cookies.set(
        "qab_rt",
        response.data.tokens.refresh,
        rememberMe.value ? "7d" : "",
        "",
        "",
        true
      );
      localStorage.setItem(
        "shouldRefreshAt",
        new Date().getTime() + 55 * 60 * 1000
      );
      if (rememberMe.value)
        localStorage.setItem("rememberMe", rememberMe.value);
      if (response.data.role === 'ADMIN') {
        window.location.href = '/admin'
      } else {
        window.location.href = '/courses'
      }
    })
    .catch((error) => {
      if (error.response) {
        for (const property in error.response.data) {
          errors.push(`${property}: ${error.response.data[property]}`);
        }
      } else if (error.message) {
        errors.push("Something went wrong. Please try again!");
      }
    });
  isLoading.value = false;
}

function submitForm(event) {
  if (event.keyCode === 13) {
    login("email");
  }
}
const callback = async (response) => {
  login("google", response.credential);
};
</script>
