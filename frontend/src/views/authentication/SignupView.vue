<template>
  <v-snackbar
    v-model="snackbar"
    :absolute="true"
    :timeout="5000"
    color="success"
    class="custom-snackbar"
  >
    Almost done! You have to verify your email. Please, check your inbox!
  </v-snackbar>
  <AuthBoard>
    <template v-slot:page-name> Sign up </template>
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
        class="medium-text"
        variant="outlined"
        @keyup="submitForm($event)"
      ></v-text-field>
      <v-text-field
        v-model="full_name"
        clearable
        label="Full name"
        prepend-inner-icon="mdi-account"
        type="text"
        class="medium-text"
        variant="outlined"
        @keyup="submitForm($event)"
      ></v-text-field>
      <v-text-field
        v-model="password1"
        label="Password"
        prepend-inner-icon="mdi-lock"
        :append-inner-icon="!showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        class="medium-text"
        variant="outlined"
        @keyup="submitForm($event)"
        @click:append-inner="showPassword = !showPassword"
      ></v-text-field>
      <v-text-field
        v-model="password2"
        label="Confirm password"
        prepend-inner-icon="mdi-lock"
        :append-inner-icon="!showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        class="medium-text"
        variant="outlined"
        @keyup="submitForm($event)"
        @click:append-inner="showPassword = !showPassword"
      ></v-text-field>
    </template>
    <template v-slot:actions>
      <div class="w-100 d-flex justify-space-evenly mb-4 px-4">
        <v-btn
          variant="tonal"
          :loading="isLoading"
          :disabled="isLoading"
          color="secondary"
          :block="true"
          class="medium-text auth-btns"
          @click="signup"
        >
          Sign up
        </v-btn>
      </div>
      <div class="my-4">
        <GoogleLogin :callback="callback" />
      </div>
      <div class="w-100 d-flex justify-space-evenly">
        <router-link
          :to="{ name: 'login' }"
          class="text-secondary text-decoration-none auth-links"
          >Already have an account?</router-link
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
import { useRouter } from "vue-router";
const router = useRouter();
const store = useStore();
const $cookies = inject("$cookies");
const errors = reactive([]);
const email = ref("");
const full_name = ref("");
const password1 = ref("");
const password2 = ref("");
const snackbar = ref(false);
const showPassword = ref(false);
const isLoading = ref(false);

async function signup() {
  isLoading.value = true;
  errors.length = 0;
  if (password1.value !== password2.value) {
    errors.push("Password and Confirm password does not match.");
    isLoading.value = false;
    return;
  }
  const formData = {
    email: email.value,
    full_name: full_name.value,
    password: password1.value,
  };
  await axios
    .post("/auth/signup/", formData)
    .then((response) => {
      response;
      snackbar.value = true;
      setTimeout(() => {
        router.push({ name: "login" });
      }, 5000);
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
    signup();
  }
}

const callback = async (response) => {
  isLoading.value = true;
  errors.length = 0;
  axios.defaults.headers.common["Authorization"] = "";
  $cookies.remove("qab_at");
  $cookies.remove("qab_rt");
  store.commit("initializeStore", {});
  localStorage.clear();
  const formData = { id_token: response.credential };
  await axios
    .post("/auth/google/", formData)
    .then((response) => {
      store.commit("initializeStore", response.data.tokens);
      store.commit("setUser", response.data);
      axios.defaults.headers.common["Authorization"] =
        "Bearer " + response.data.tokens.access;
      $cookies.set("qab_at", response.data.tokens.access, "", "", "", true);
      $cookies.set("qab_rt", response.data.tokens.refresh, "", "", "", true);
      localStorage.setItem(
        "shouldRefreshAt",
        new Date().getTime() + 55 * 60 * 1000
      );
      router.push({ name: "courses" });
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
};
</script>
