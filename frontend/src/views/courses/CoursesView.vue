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
        ><p class="ma-1 page-text">My courses</p></v-col
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
    <v-row v-if="user.role === 'STUDENT'" class="ma-1">
      <v-col cols="12" class="pa-0 explore-btn">
        <v-btn
          color="secondary"
          height="50px"
          :block="true"
          @click="router.push({ name: 'explore' })"
        >
          + Explore <br />
          new courses
        </v-btn>
      </v-col>
    </v-row>
    <v-row v-else class="ma-1">
      <v-col cols="12" class="pa-0 explore-btn">
        <v-btn color="secondary" height="50px" :block="true">
          + Create <br />
          new course
          <v-dialog
            v-model="createCourseDialog"
            activator="parent"
            max-width="480px"
          >
            <v-card color="secondary">
              <v-card-title>New course</v-card-title>
              <v-card-text class="pa-3">
                <v-form ref="createCourseForm">
                  <v-text-field
                    v-model="name"
                    label="Course name"
                    density="comfortable"
                    :rules="[(v) => !!v || 'This field is required']"
                  ></v-text-field>
                  <v-text-field
                    v-model="semester"
                    label="Semester"
                    density="comfortable"
                    :rules="[(v) => !!v || 'This field is required']"
                  ></v-text-field>
                  <v-text-field
                    v-model="startedAt"
                    type="date"
                    label="Started at"
                    density="comfortable"
                    :rules="[(v) => !!v || 'This field is required']"
                  ></v-text-field>
                  <v-autocomplete
                    v-model="selectedStudents"
                    :items="students"
                    chips
                    closable-chips
                    density="comfortable"
                    item-title="full_name"
                    item-value="id"
                    label="Invite students"
                    multiple
                    hide-details
                    :custom-filter="customFilter"
                    :menu-props="{ theme: 'dark' }"
                  >
                  </v-autocomplete>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  color="primary"
                  @click="createCourse"
                  :loading="createCourseLoading"
                  :disabled="createCourseLoading"
                >
                  Submit
                </v-btn>
                <v-btn color="primary" @click="createCourseDialog = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-btn>
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
        <router-link
          :to="`/courses/${course.id}`"
          class="course-detail-router-link"
        >
          <v-card class="bg-secondary ma-1 course-card" variant="plain">
            <v-card-title class="course-name">
              <v-badge
                v-if="
                  store.state.notifications
                    .filter((n) => !n.is_seen)
                    .filter(
                      (n) =>
                        n.name === 'STUDENT_NEW_ANSWER' ||
                        n.name === 'PROFESSOR_NEW_QUESTION'
                    )
                    .filter((n) => n.course.id === course.id).length > 0
                "
                dot
                inline
                color="error"
              ></v-badge>
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
              <p>Given questions: {{ course.given_questions }}</p>
              <p>Answered: {{ course.answered }}</p>
            </v-card-text>
            <v-card-text class="text-right">
              <v-icon
                v-if="course.is_completed"
                icon="mdi-check-circle"
                class="text-success"
              ></v-icon>
              <v-icon v-else icon="mdi-clock" class="text-warning"></v-icon>
              {{ course.is_completed ? "Completed" : "In progress" }}
            </v-card-text>
          </v-card>
        </router-link>
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
const createCourseDialog = ref(false);
const name = ref("");
const semester = ref("");
const startedAt = ref("");
const selectedStudents = ref([]);
const students = ref([]);
const createCourseForm = ref(null);
const createCourseLoading = ref(false);

const snackbar = reactive({
  isOpen: false,
  color: "",
  content: "",
});

const user = computed(() => store.getters.getUser);

watch(search, async (newValue, oldValue) => {
  await axios.get(`/course/?search=${newValue}`).then((response) => {
    courses.value = response.data;
  });
  oldValue;
});

onMounted(async () => {
  await axios
    .get("/course/")
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
  await axios
    .get("/course/students/")
    .then((response) => {
      students.value = response.data;
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

async function createCourse() {
  const form = await createCourseForm.value.validate();
  if (form.valid) {
    createCourseLoading.value = true;
    await axios
      .post("/course/", {
        name: name.value,
        semester: semester.value,
        started_at: startedAt.value,
        students: selectedStudents.value,
      })
      .then((response) => {
        const newCourse = response.data;
        newCourse.students = selectedStudents.value.length;
        courses.value.unshift(newCourse);
        name.value = "";
        semester.value = "";
        startedAt.value = "";
        selectedStudents.value = [];
        createCourseDialog.value = false;
        createCourseLoading.value = false;
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
}

function getProfessorInitials(professor) {
  return professor.full_name
    .trim()
    .split(" ")
    .map((name) => name[0])
    .join("")
    .toUpperCase();
}

function customFilter(value, query, item) {
  item;
  return value.full_name.indexOf(query) > -1;
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
.course-detail-router-link {
  text-decoration: none !important;
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
.explore-btn .v-btn {
  font-size: 24px;
  text-transform: none;
  line-height: 20px;
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