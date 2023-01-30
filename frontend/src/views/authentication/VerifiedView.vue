<template>
  <AuthBoard>
    <template v-slot:default>
      <p class="medium-text">Congratulations on verifying your account! You can now log into your account.</p>
    </template>
    <template v-slot:actions>
      <router-link
        :to="{ name: 'login' }"
        class="text-secondary text-decoration-none auth-links"
        >Go to login</router-link
      >
    </template>
  </AuthBoard>
</template>

<script setup>
import AuthBoard from "@/components/AuthBoard.vue";
</script>
