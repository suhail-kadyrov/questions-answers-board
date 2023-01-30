<template>
  <AuthBoard>
    <template v-slot:default>
      <p class="text-h1 text-center text-warning">
        404
      </p>
      <p class="text-h4 text-center text-warning mb-4">
        Page not found
      </p>
    </template>
    <template v-slot:actions>
      <router-link
        to="/"
        class="text-secondary text-decoration-none auth-links"
      >
        Go back
      </router-link>
    </template>
  </AuthBoard>
</template>

<script setup>
import AuthBoard from "@/components/AuthBoard.vue";
</script>
