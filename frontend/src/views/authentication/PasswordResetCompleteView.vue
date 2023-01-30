<template>
  <v-snackbar
    v-model="snackbar"
    :absolute="true"
    :timeout="3000"
    color="success"
    class="custom-snackbar"
  >
    You can now log in with your new password!
  </v-snackbar>
  <AuthBoard v-if="isValid">
    <template v-slot:page-name> Password reset </template>
    <template v-slot:default>
      <v-alert v-if="errors.length" type="error" class="mb-4 medium-text">
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </v-alert>
      <p class="text-subtitle-1">Enter new password</p>
      <v-text-field
        v-model="password1"
        clearable
        label="Password"
        prepend-inner-icon="mdi-lock"
        type="password"
        class="medium-text"
        variant="outlined"
        @keyup="submitForm($event)"
      ></v-text-field>
      <v-text-field
        v-model="password2"
        clearable
        label="Confirm password"
        prepend-inner-icon="mdi-lock"
        type="password"
        class="medium-text"
        variant="outlined"
        @keyup="submitForm($event)"
      ></v-text-field>
    </template>
    <template v-slot:actions>
      <div class="w-100 px-4 mb-4">
        <v-btn
          variant="tonal"
          color="secondary"
          :block="true"
          class="medium-text auth-btns"
          :loading="isLoading"
          :disabled="isLoading"
          @click="callback"
        >
          Set new password
        </v-btn>
      </div>
      <div class="w-100 d-flex justify-space-evenly">
        <router-link
          :to="{ name: 'login' }"
          class="text-secondary text-decoration-none auth-links"
          >Back to login</router-link
        >
      </div>
    </template>
  </AuthBoard>
  <AuthBoard v-else>
    <template v-slot:default>
      <p class="medium-text">
        You used a link that is either broken or no longer active.
      </p>
    </template>
    <template v-slot:actions>
      <router-link
        :to="{ name: 'login' }"
        class="text-secondary text-decoration-none auth-links"
        >Back to login</router-link
      >
    </template>
  </AuthBoard>
</template>

<script setup>
import AuthBoard from "@/components/AuthBoard.vue";
import axios from "axios";
import { ref, onMounted, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
const router = useRouter();
const route = useRoute();
const password1 = ref("");
const password2 = ref("");
const errors = reactive([]);
const snackbar = ref(false);
const isValid = ref(false);
const isLoading = ref(false);

onMounted(() => {
  isValid.value = route.query.token && route.query.uidb64;
});

async function callback() {
  isLoading.value = true;
  errors.length = 0;
  if (password1.value !== password2.value) {
    errors.push("Password and Confirm password does not match.");
    isLoading.value = false;
    return;
  }
  const formData = {
    password: password1.value,
    token: route.query.token,
    uidb64: route.query.uidb64,
  };
  await axios
    .patch("/auth/reset_password_complete/", formData)
    .then((response) => {
      response;
      snackbar.value = true;
      setTimeout(() => {
        router.push({ name: "login" });
      }, 3000);
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
    callback();
  }
}
</script>

<style lang="scss">
.custom-snackbar .v-overlay__content {
  top: 0 !important;
  .v-snackbar__content {
    font-size: 1.2rem !important;
  }
}
</style>