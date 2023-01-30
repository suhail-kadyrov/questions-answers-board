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
    <v-row>
      <v-col cols="12" sm="8" class="pt-1 pb-0"
        ><p class="ma-1 page-text">New courses</p></v-col
      >
      <v-col cols="12" sm="4">
        <v-text-field
          v-model="search"
          label="Search ..."
          variant="outlined"
          class="medium-text"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col
        v-for="course in courses"
        :key="course.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card class="bg-secondary ma-1 course-card" variant="plain">
          <v-card-title class="course-name">
            {{ course.name }}
            <v-tooltip activator="parent" location="top" :offset="-25">
              {{ course.name }}
            </v-tooltip>
          </v-card-title>
          <v-card-title v-if="user.role === 'STUDENT'" class="pt-0">
            <v-avatar
              :image="course.professor.image"
              size="50"
              class="bg-primary"
            >
              {{ getProfessorInitials(course.professor) }}
            </v-avatar>
            <span class="professor-name">
              {{ course.professor.full_name }}
              <v-tooltip activator="parent" location="top" :offset="-5">
                {{ course.professor.full_name }}
              </v-tooltip>
            </span>
          </v-card-title>
          <v-card-text class="course-info py-0">
            <p>Semester: {{ course.semester }}</p>
            <p>Started at: {{ course.started_at }}</p>
            <p>Students: {{ course.students }}</p>
          </v-card-text>
          <v-card-text class="text-right">
            <v-btn
              prepend-icon="mdi-account-supervisor-circle-outline"
              size="small"
              variant="tonal"
              @click="sendEnrollmentRequest(course.id)"
            >
              Enroll
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <!-- <v-row justify="center">
      <v-col cols="8" class="pb-0">
        <v-container class="max-width pb-0">
          <v-pagination v-model="page" class="my-4" :length="60"></v-pagination>
        </v-container>
      </v-col>
    </v-row> -->
  </v-container>
</template>

<script setup>
import MainHaeder from "@/components/MainHeader.vue";
import axios from "axios";
import { onMounted, ref, reactive, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
const store = useStore();
const router = useRouter();
// const page = ref(1);
const search = ref("");
const courses = ref([]);

const snackbar = reactive({
  isOpen: false,
  color: "",
  content: "",
});

const user = computed(() => store.getters.getUser);

watch(search, async (newValue, oldValue) => {
  await axios.get(`/course/explore/?search=${newValue}`).then((response) => {
    courses.value = response.data;
  });
  oldValue;
});

onMounted(async () => {
  await axios
    .get("/course/explore/")
    .then((response) => {
      courses.value = response.data;
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
});

async function sendEnrollmentRequest(courseID) {
  await axios
    .post(`/notifications/student/enrollment/${courseID}/sent/`)
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

function getProfessorInitials(professor) {
  return professor.full_name
    .trim()
    .split(" ")
    .map((name) => name[0])
    .join("")
    .toUpperCase();
}
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
  font-size: 54px;
  font-weight: 300;
  line-height: 75px;
  margin-top: 0 !important;
}
.course-card {
  background-color: #ebf6f2 !important;
  color: #002b59 !important;
}
.course-info {
  p {
    font-size: 20px;
    font-weight: 300;
    line-height: 30px;
    margin: 5px 0;
  }
}
.course-name {
  font-size: 28px;
  font-weight: 700;
  line-height: 50px;
}
.professor-name {
  margin-left: 10px;
  font-size: 24px;
  font-weight: 300;
}
@media only screen and (max-width: 650px) {
  #container {
    margin-top: 80px;
    height: calc(100vh - 80px);
  }
  .page-text {
    font-size: 48px;
  }
}
</style>