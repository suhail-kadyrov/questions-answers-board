<template>
  <v-container class="py-0">
    <v-row justify="center">
      <v-col id="auth-board">
        <v-card class="py-4">
          <v-card-title class="text-h5 text-center arial">
            Questions & Answers Board
          </v-card-title>
          <v-card-subtitle class="text-h6 text-center py-2 arial">
            <slot name="page-name"></slot>
          </v-card-subtitle>
          <v-card-text>
            <slot></slot>
          </v-card-text>
          <v-card-actions class="flex-column">
            <slot name="actions"></slot>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
#auth-board {
  height: 100vh;
  max-width: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  .v-card {
    width: 100%;
    box-shadow: -20px 20px 50px 10px rgba(0, 0, 0, 0.25);
  }
}
.arial {
  font-family: "Arial", sans-serif !important;
}
</style>