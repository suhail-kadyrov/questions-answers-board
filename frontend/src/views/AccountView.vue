<template>
  <v-snackbar
    v-model="snackbar.isOpen"
    :absolute="true"
    :timeout="2000"
    :color="snackbar.color"
    class="custom-snackbar"
  >
    {{ snackbar.content }}
  </v-snackbar>
  <MainHaeder />
  <v-container class="bg-primary" id="container">
    <p class="page-text">
      <span>Account settings</span>
      <span class="page-text__btns">
        <v-btn
          v-if="user.role === 'STUDENT'"
          variant="text"
          color="secondary"
          @click="sendPromotionRequest"
        >
          <v-icon icon="mdi-briefcase"></v-icon>
          <v-tooltip activator="parent" location="start">
            Become a professor
          </v-tooltip>
        </v-btn>
        <!-- <v-btn variant="text" color="secondary" prepend-icon="mdi-translate">
          En
          <v-menu activator="parent">
            <v-list class="bg-white" density="compact">
              <v-list-item v-for="m in 3" :key="m" :value="m">
                Lang {{ m }}
              </v-list-item>
            </v-list>
          </v-menu>
        </v-btn> -->
        <v-btn
          variant="text"
          color="warning"
          append-icon="mdi-exit-to-app"
          :loading="isLoading"
          :disabled="isLoading"
          @click="logout"
        >
          Log out
        </v-btn>
      </span>
    </p>
    <div class="d-flex flex-column align-center">
      <span class="avatar-container">
        <v-avatar :image="user.image" size="80">
          {{ userInitials }}
        </v-avatar>
        <p class="medium-text mt-2">{{ user.full_name }}</p>
        <span class="avatar-delete" @click="removeAvatar">
          <v-icon icon="mdi-delete"></v-icon>
        </span>
        <label for="avatar-input" class="avatar-upload">
          <v-icon icon="mdi-upload"></v-icon>
        </label>
      </span>
    </div>
    <p class="mb-2">Personal info</p>
    <v-row class="align-center">
      <v-file-input
        id="avatar-input"
        style="display: none"
        accept="image/*"
        @change="setAvatar"
      ></v-file-input>
      <v-col cols="10" sm="11">
        <v-text-field
          v-model="fullName"
          clearable
          prepend-inner-icon="mdi-account"
          label="Full name"
          density="compact"
          variant="outlined"
          hide-details
          @keyup="submitForm($event, 'name')"
        ></v-text-field>
      </v-col>
      <v-col cols="2" sm="1">
        <v-btn
          variant="text"
          :loading="isLoading"
          :disabled="isLoading"
          icon="mdi-check"
          class="acc-page-btns"
          @click="changeData('name')"
        >
        </v-btn>
      </v-col>
    </v-row>
    <hr class="my-2" />
    <template v-if="user.auth_provider === 'email'">
      <p>Email</p>
      <p class="text-warning mb-2">
        If you change your email, you will have to verify it. Otherwise, you
        cannot log into your account again.
      </p>
      <v-row class="align-center">
        <v-col cols="12" sm="6">
          <v-text-field
            v-model="email"
            clearable
            prepend-inner-icon="mdi-email"
            density="compact"
            label="Email"
            variant="outlined"
            hide-details
            @keyup="submitForm($event, 'email')"
          ></v-text-field>
        </v-col>
        <v-col cols="10" sm="5">
          <v-text-field
            v-model="password"
            clearable
            prepend-inner-icon="mdi-lock"
            density="compact"
            label="Password"
            variant="outlined"
            type="password"
            hide-details
            @keyup="submitForm($event, 'email')"
          ></v-text-field>
        </v-col>
        <v-col cols="2" sm="1">
          <v-btn
            variant="text"
            :loading="isLoading"
            :disabled="isLoading"
            icon="mdi-check"
            class="acc-page-btns"
            @click="changeData('email')"
          >
          </v-btn>
        </v-col>
      </v-row>
      <hr class="my-2" />
      <p>Password</p>
      <p class="text-warning mb-2">
        You must enter your current password to change it.
      </p>
      <v-row class="align-center">
        <v-col cols="12" sm="3">
          <v-text-field
            v-model="oldPassword"
            clearable
            prepend-inner-icon="mdi-lock"
            density="compact"
            label="Current password"
            variant="outlined"
            type="password"
            hide-details
            @keyup="submitForm($event, 'password')"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field
            v-model="newPassword1"
            clearable
            prepend-inner-icon="mdi-lock"
            density="compact"
            label="New password"
            variant="outlined"
            type="password"
            hide-details
            @keyup="submitForm($event, 'password')"
          ></v-text-field>
        </v-col>
        <v-col cols="10" sm="4">
          <v-text-field
            v-model="newPassword2"
            clearable
            prepend-inner-icon="mdi-lock"
            density="compact"
            label="Confirm password"
            variant="outlined"
            type="password"
            hide-details
            @keyup="submitForm($event, 'password')"
          ></v-text-field>
        </v-col>
        <v-col cols="2" sm="1">
          <v-btn
            variant="text"
            :loading="isLoading"
            :disabled="isLoading"
            icon="mdi-lock-reset"
            class="acc-page-btns"
            @click="changeData('password')"
          >
          </v-btn>
        </v-col>
      </v-row>
    </template>
    <template v-else>
      <p class="mb-2">
        You can change your Google account. Current: {{ user.email }}
      </p>
      <GoogleLogin :callback="callback" />
    </template>
  </v-container>
</template>

<script setup>
import MainHaeder from "@/components/MainHeader.vue";
import axios from "axios";
import { ref, reactive, computed, onMounted, inject } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
const router = useRouter();
const store = useStore();
const $cookies = inject("$cookies");
const fullName = ref("");
const email = ref("");
const password = ref("");
const oldPassword = ref("");
const newPassword1 = ref("");
const newPassword2 = ref("");
const snackbar = reactive({
  isOpen: false,
  color: "",
  content: "",
});

const user = computed(() => store.getters.getUser);
const userInitials = computed(() =>
  store.getters.getUser.full_name
    .trim()
    .split(" ")
    .map((name) => name[0])
    .join("")
    .toUpperCase()
);
const isLoading = ref(false);

onMounted(async () => {
  await axios
    .get("/profile/")
    .then((response) => {
      store.commit("setUser", response.data);
      email.value = response.data.email;
      fullName.value = response.data.full_name;
    })
    .catch((error) => {
      error;
      store.commit("initializeStore", {});
      router.push({ name: "login" });
    });
});

async function changeData(action) {
  isLoading.value = true;
  snackbar.isOpen = false;
  let config = {};
  if (action === "name") {
    config = {
      url: "/profile/",
      method: "put",
      data: {
        full_name: fullName.value,
      },
    };
  } else if (action === "email") {
    config = {
      url: "/profile/set_email/",
      method: "patch",
      data: {
        email: email.value,
        password: password.value,
      },
    };
  } else if (action === "password") {
    if (newPassword1.value !== newPassword2.value) {
      snackbar.content = "Password and Confirm password does not match.";
      snackbar.color = "error";
      snackbar.isOpen = true;
      isLoading.value = false;
      return;
    }
    config = {
      url: "/profile/set_password/",
      method: "patch",
      data: {
        old_password: oldPassword.value,
        new_password: newPassword1.value,
      },
    };
  }
  await axios
    .request(config)
    .then((response) => {
      if (action === "name") {
        snackbar.content = "Success!";
        snackbar.color = "success";
        snackbar.isOpen = true;
        store.commit("setUser", response.data);
      } else if (action === "password") {
        snackbar.content = "Success!";
        snackbar.color = "success";
        snackbar.isOpen = true;
        oldPassword.value = "";
        newPassword1.value = "";
        newPassword2.value = "";
      } else {
        snackbar.content = "Please, verify your new email!";
        snackbar.color = "info";
        snackbar.isOpen = true;
        setTimeout(() => {
          store.commit("initializeStore", {});
          router.push({ name: "login" });
        }, 1000);
      }
    })
    .catch((error) => {
      if (error.response) {
        if (error.response.status === 401) {
          store.commit("initializeStore", {});
          router.push({ name: "login" });
        } else {
          snackbar.content = "";
          for (const property in error.response.data) {
            snackbar.content += `${property}: ${error.response.data[property]}\n`;
          }
          snackbar.color = "error";
          snackbar.isOpen = true;
        }
      } else if (error.message) {
        snackbar.content = "Something went wrong. Please try again!";
        snackbar.color = "error";
        snackbar.isOpen = true;
      }
    });
  isLoading.value = false;
}

function submitForm(event, action) {
  if (event.keyCode === 13) {
    changeData(action);
  }
}

async function setAvatar(event) {
  let formData = new FormData();
  isLoading.value = true;
  formData.append("image", event.target.files[0]);
  await axios
    .patch("/profile/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => {
      store.state.user.image = response.data.image;
    });
  isLoading.value = false;
}

async function removeAvatar() {
  await axios.patch("/profile/").then((response) => {
    response;
    store.state.user.image = null;
  });
}

async function sendPromotionRequest() {
  await axios
    .post("/notifications/professor/promotion/sent/")
    .then((response) => {
      response;
      snackbar.content = "Your request has sent!";
      snackbar.color = "success";
      snackbar.isOpen = true;
    })
    .catch((error) => {
      if (error.response && error.response.status === 401) {
        store.commit("initializeStore", {});
        router.push({ name: "login" });
      } else if (error.message) {
        snackbar.content = error.message;
        snackbar.color = "error";
        snackbar.isOpen = true;
      }
    });
}

async function logout() {
  isLoading.value = true;
  await axios
    .post("/auth/logout/", {
      refresh: $cookies.get("qab_rt"),
    })
    .then((response) => {
      response;
      store.commit("initializeStore", {});
      router.push({ name: "login" });
    })
    .catch((error) => {
      error;
      store.commit("initializeStore", {});
      router.push({ name: "login" });
    });
  isLoading.value = false;
}

const callback = async (response) => {
  await axios
    .put("/profile/set_gmail/", {
      id_token: response.credential,
    })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      if (error.response) {
        if (error.response.status === 401) {
          store.commit("initializeStore", {});
          router.push({ name: "login" });
        } else {
          snackbar.content = "";
          for (const property in error.response.data) {
            snackbar.content += `${property}: ${error.response.data[property]}\n`;
          }
          snackbar.color = "error";
          snackbar.isOpen = true;
        }
      } else if (error.message) {
        snackbar.content = "Something went wrong. Please try again!";
        snackbar.color = "error";
        snackbar.isOpen = true;
      }
    });
};
</script>

<style lang="scss" scoped>
#container {
  margin-top: 110px;
  border-radius: 20px;
  height: calc(100vh - 110px);
  overflow: auto;
}

#container::-webkit-scrollbar-track {
  background-color: #ffffff00;
  border-radius: 10px;
  border: none;
}

#container::-webkit-scrollbar {
  width: 10px;
  background-color: #ffffff00;
}

#container::-webkit-scrollbar-thumb {
  border-radius: 10px;
  border: none;
  background-color: #ffffff00;
  background-image: -webkit-gradient(
    linear,
    40% 0%,
    75% 84%,
    from(#06534200),
    to(#06534200),
    color-stop(0.6, #ebf6f2)
  );
}
.page-text {
  font-size: 36px;
  font-weight: 300;
  line-height: 36px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  button {
    font-size: 20px;
    text-transform: none;
  }
}
.acc-page-btns {
  font-size: 24px;
  text-transform: none;
}
.avatar-container {
  position: relative;
  text-align: center;
  .v-avatar {
    border: 1px solid white;
    font-size: 32px;
  }
}
.avatar- {
  &delete,
  &upload {
    background-color: white;
    border-radius: 50%;
    padding: 2px;
    position: absolute;
    top: 0;
    cursor: pointer;
    &:hover {
      background-color: #ccc;
    }
  }
  &delete {
    color: red;
    right: calc(calc(100% - 100px) / 2);
  }
  &upload {
    color: blue;
    left: calc(calc(100% - 100px) / 2);
  }
}
@media only screen and (max-width: 650px) {
  #container {
    margin-top: 80px;
    height: calc(100vh - 80px);
  }
  .page-text {
    flex-direction: column-reverse;
  }
  .page-text__btns {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
}
</style>