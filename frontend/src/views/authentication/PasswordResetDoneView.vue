<template>
  <AuthBoard>
    <template v-slot:default>
      <p class="medium-text">Check your inbox. We have sent you a link to reset your password.</p>
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
</script>
