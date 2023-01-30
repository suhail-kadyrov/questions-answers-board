<template>
  <v-container class="bg-primary" id="header">
    <div class="header__left">
      <div class="logo">Logo</div>
      <p>Q&A Board</p>
    </div>
    <div class="header__right">
      <router-link v-if="store.getters.getUser.role !== 'ADMIN'" :to="{ name: 'courses' }">
        <v-icon icon="mdi-notebook"></v-icon>
      </router-link>
      <router-link v-else :to="{ name: 'admin-dashboard' }">
        <v-icon icon="mdi-view-dashboard"></v-icon>
      </router-link>
      <span id="notification-bell">
        <v-icon icon="mdi-bell" id="notifications-activator"></v-icon>
        <span
          v-if="store.state.notifications.filter((n) => !n.is_seen).length > 0"
          id="notification-indicator"
        ></span>
      </span>
      <v-menu activator="#notifications-activator">
        <v-list
          id="notifications-list"
          lines="two"
          class="bg-secondary"
          max-height="250px"
        >
          <v-list-item
            v-for="notification in store.state.notifications"
            :key="notification.id"
            :value="notification.id"
            density="compact"
            style="z-index: 1001"
            max-width="400px"
            class="py-0"
            @click="seeNotification(notification.id)"
          >
            <v-badge
              v-if="!notification.is_seen"
              dot
              inline
              color="error"
            ></v-badge>
            <span>
              <a href="javascript:void(0)">
                {{ notification.text }}
              </a>
              <span
                v-if="
                  notification.name === 'PROFESSOR_ENROLMENT_REQUEST' ||
                  notification.name === 'ADMIN_PROMOTION_REQUEST'
                "
                class="ml-1"
              >
                <v-btn
                  prepend-icon="mdi-check-circle-outline"
                  size="x-small"
                  variant="tonal"
                  color="success"
                  @click="accept(notification)"
                >
                  Accept
                </v-btn>
                <v-btn
                  prepend-icon="mdi-check-circle-outline"
                  size="x-small"
                  variant="tonal"
                  color="error"
                  @click="reject(notification)"
                >
                  Reject
                </v-btn>
              </span>
            </span>
            <p class="text-right">
              <small>{{
                new Date(notification.sent_at).toLocaleString("en-GB", {
                  timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                })
              }}</small>
            </p>
            <hr class="ma-0" />
          </v-list-item>
        </v-list>
      </v-menu>
      <router-link :to="{ name: 'account' }">
        <v-avatar :image="user.image" size="48">{{ userInitials }}</v-avatar>
      </router-link>
    </div>
  </v-container>
</template>

<script setup>
import axios from "axios";
import { computed } from "vue";
import { useStore } from "vuex";
const store = useStore();
// const dialog = ref(false);
const user = computed(() => store.getters.getUser);
const userInitials = computed(() =>
  store.getters.getUser.full_name
    .trim()
    .split(" ")
    .map((name) => name[0])
    .join("")
    .toUpperCase()
);

async function seeNotification(ntfID) {
  await axios.patch(`/notifications/seen/${ntfID}/`).then((response) => {
    response;
    store.state.notifications.filter((n) => n.id === ntfID)[0].is_seen = true;
  });
}

async function accept(ntf) {
  let url = "";
  let formData = null;
  if (ntf.name === "PROFESSOR_ENROLMENT_REQUEST") {
    url = "/notifications/student/enroll/answer/";
    formData = {
      course: ntf.course.id,
      user: ntf.user.id,
    };
  } else if (ntf.name === "ADMIN_PROMOTION_REQUEST") {
    url = "/notifications/professor/promotion/answer/";
    formData = {
      user: ntf.user.id,
    };
  }

  await axios.put(url, formData)
}

async function reject(ntf) {
  let url = "";
  let formData = null;
  if (ntf.name === "PROFESSOR_ENROLMENT_REQUEST") {
    url = "/notifications/student/enroll/answer/";
    formData = {
      course: ntf.course.id,
      user: ntf.user.id,
    };
  } else if (ntf.name === "ADMIN_PROMOTION_REQUEST") {
    url = "/notifications/professor/promotion/answer/";
    formData = {
      user: ntf.user.id,
    };
  }
  await axios.patch(url, formData)
}
</script>

<style lang="scss" scoped>
#header {
  height: 100px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  border-radius: 20px;
  position: fixed;
  left: 50%;
  transform: translate(-50%, 0);
  z-index: 1000;
  p {
    font-size: 48px;
    font-weight: 700;
  }
}
.header__ {
  &left {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
  &right {
    font-size: 32px;
    a {
      color: white;
      text-decoration: none;
    }
    .v-avatar {
      border: 1px solid white;
      transition: 0.05s;
      &:hover {
        border-radius: 5px;
      }
    }
    i {
      margin-right: 25px;
      cursor: pointer;
      &:hover {
        border: 1px solid white;
        border-radius: 10px;
      }
    }
  }
}
.logo {
  width: 70px;
  height: 70px;
  background-color: white;
  color: #065342;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 24px;
  font-weight: 700;
  margin-right: 30px;
}
.router-link-exact-active {
  i {
    border: 1px solid white;
    border-radius: 10px;
  }
  .v-avatar {
    border-radius: 10px;
  }
}
#notifications-list {
  scrollbar-width: thin !important;
  &::-webkit-scrollbar {
    width: 3px;
  }
  &::-webkit-scrollbar-track {
    border-radius: 10px;
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background-color: #06534299;
  }
}
#notification-bell {
  position: relative;
  #notification-indicator {
    position: absolute;
    top: 0;
    left: 0;
    border-radius: 50%;
    background-color: red;
    display: inline-block;
    width: 10px;
    height: 10px;
  }
}
@media only screen and (max-width: 650px) {
  #header {
    height: 70px;
    p,
    i {
      font-size: 1.3rem;
    }
    .v-avatar {
      font-size: 15px;
    }
  }
  .logo {
    width: 48px;
    height: 48px;
    margin-right: 10px;
    font-size: 16px;
  }
  .v-avatar {
    height: 25px !important;
    width: 25px !important;
  }
  #container {
    margin-top: 80px;
  }
}
</style>