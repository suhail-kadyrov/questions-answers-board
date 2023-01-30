<template>
  <AuthBoard>
    <template v-slot:page-name> Password reset </template>
    <template v-slot:default>
      <v-alert v-if="errors.length" type="error" class="mb-4 medium-text">
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </v-alert>
      <p class="text-subtitle-1">Enter your email to reset your password</p>
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
    </template>
    <template v-slot:actions>
      <div class="w-100 px-4 mb-4">
        <v-btn
          variant="tonal"
          color="secondary"
          :loading="isLoading"
          :disabled="isLoading"
          :block="true"
          class="medium-text auth-btns"
          @click="callback"
        >
          Send reset link
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
</template>

<script setup>
import AuthBoard from "@/components/AuthBoard.vue";
import axios from "axios";
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const email = ref("");
const errors = reactive([]);
const isLoading = ref(false);

async function callback() {
  isLoading.value = true;
  errors.length = 0;
  await axios
    .post("/auth/reset_password/", { email: email.value })
    .then((response) => {
      response;
      router.push({ name: "reset-password-done" });
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
