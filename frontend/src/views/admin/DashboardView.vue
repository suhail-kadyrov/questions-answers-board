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
      <v-col cols="12" sm="8" class="pt-1 pb-0">
        <p class="ma-2 page-text">
          <v-btn
            icon="mdi-power"
            variant="tonal"
            class="mr-3"
            :class="{
              'text-success': autoAnswering,
              'text-error': !autoAnswering,
            }"
            :loading="loadings.autoAnswering"
            :disabled="loadings.autoAnswering"
            @click="toggleAutoAnswering"
          ></v-btn>
          Auto answering: {{ autoAnswering ? "ON" : "OFF" }}
        </p>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12" md="4" class="px-2 mt-4">
        <div class="main-blocks pa-3">
          <v-expansion-panels
            v-model="coursesPanel"
            variant="accordion"
            @update:modelValue="getCourses"
          >
            <v-expansion-panel class="bg-secondary">
              <v-expansion-panel-title class="font-weight-bold">
                COURSES
                <v-progress-circular
                  v-if="loadings.getCourses"
                  color="primary"
                  :size="20"
                  :width="2"
                  class="ml-3"
                  indeterminate
                ></v-progress-circular>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="main-blocks__items">
                <v-text-field
                  v-model="searchCourses"
                  label="Search ..."
                  variant="outlined"
                  density="compact"
                  class="medium-text"
                  hide-details
                ></v-text-field>
                <v-card
                  v-for="course in courses"
                  :key="course.id"
                  variant="tonal"
                  class="my-1"
                  @click="showModifyCourseDialog(course.id)"
                >
                  <v-card-text class="text-center">
                    <b>{{ course.name }} ({{ course.semester }})</b>
                    <br />
                    Students: {{ course.students }}
                  </v-card-text>
                </v-card>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </v-col>
      <v-col cols="12" md="4" class="px-2 mt-4">
        <div class="main-blocks pa-3">
          <v-expansion-panels
            v-model="professorsPanel"
            variant="accordion"
            @update:modelValue="getProfessors"
          >
            <v-expansion-panel class="bg-secondary">
              <v-expansion-panel-title class="font-weight-bold">
                PROFESSORS
                <v-progress-circular
                  v-if="loadings.getProfessors"
                  color="primary"
                  :size="20"
                  :width="2"
                  class="ml-3"
                  indeterminate
                ></v-progress-circular>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="main-blocks__items">
                <v-text-field
                  v-model="searchProfessors"
                  label="Search ..."
                  variant="outlined"
                  density="compact"
                  class="medium-text"
                  hide-details
                ></v-text-field>
                <v-btn
                  color="secondary"
                  class="my-2"
                  :block="true"
                  @click="addProfessorDialog = true"
                  >Add new professor</v-btn
                >
                <v-card
                  v-for="professor in professors"
                  :key="professor.id"
                  variant="tonal"
                  class="my-1"
                  @dblclick="showCourses(professor)"
                >
                  <v-tooltip
                    activator="parent"
                    location="end"
                    open-delay="1000"
                  >
                    Double click to see courses
                  </v-tooltip>
                  <v-card-text class="text-center">
                    <b>{{ professor.full_name }}</b>
                    <br />
                    Courses: {{ professor.courses }}
                    <p class="text-right user-delete-btn">
                      <v-btn
                        icon="mdi-delete"
                        size="x-small"
                        variant="tonal"
                        color="error"
                        @click="deleteUser(professor)"
                      >
                      </v-btn>
                    </p>
                  </v-card-text>
                </v-card>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </v-col>
      <v-col cols="12" md="4" class="px-2 mt-4">
        <div class="main-blocks pa-3">
          <v-expansion-panels
            v-model="studentsPanel"
            variant="accordion"
            @update:modelValue="getStudents"
          >
            <v-expansion-panel class="bg-secondary">
              <v-expansion-panel-title class="font-weight-bold">
                STUDENTS
                <v-progress-circular
                  v-if="loadings.getStudents"
                  color="primary"
                  :size="20"
                  :width="2"
                  class="ml-3"
                  indeterminate
                ></v-progress-circular>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="main-blocks__items">
                <v-text-field
                  v-model="searchStudents"
                  label="Search ..."
                  variant="outlined"
                  density="compact"
                  class="medium-text"
                  hide-details
                ></v-text-field>
                <v-card
                  v-for="student in students"
                  :key="student.id"
                  variant="tonal"
                  class="my-1"
                  @dblclick="showCourses(student)"
                >
                  <v-tooltip
                    activator="parent"
                    location="end"
                    open-delay="1000"
                  >
                    Double click to see courses
                  </v-tooltip>
                  <v-card-text class="text-center">
                    <b>{{ student.full_name }}</b>
                    <br />
                    Enrolled courses: {{ student.courses }}
                    <p class="text-right user-delete-btn">
                      <v-btn
                        icon="mdi-delete"
                        size="x-small"
                        variant="tonal"
                        color="error"
                        @click="deleteUser(student)"
                      >
                      </v-btn>
                    </p>
                  </v-card-text>
                </v-card>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <v-dialog v-model="modifyCourseDialog" max-width="480px">
    <v-card color="secondary">
      <v-card-title>{{ name }}</v-card-title>
      <v-card-text class="pa-3">
        <v-form ref="editCourseForm">
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
          <v-autocomplete
            v-model="selectedProfessor"
            :items="professors"
            density="comfortable"
            item-title="full_name"
            item-value="id"
            label="Professor"
            :custom-filter="customFilter"
            :menu-props="{ theme: 'dark' }"
            :rules="[(v) => !!v || 'This field is required']"
          >
          </v-autocomplete>
          <v-autocomplete
            v-model="selectedStudents"
            :items="students"
            chips
            closable-chips
            density="comfortable"
            item-title="full_name"
            item-value="id"
            label="Students"
            multiple
            hide-details
            :custom-filter="customFilter"
            :menu-props="{ theme: 'dark' }"
          >
          </v-autocomplete>
          <v-checkbox
            v-model="isCompleted"
            label="Completed"
            hide-details
          ></v-checkbox>
        </v-form>
      </v-card-text>
      <v-card-actions
        class="d-flex flex-row justify-space-between align-center"
      >
        <span>
          <v-btn
            color="primary"
            @click="editCourse"
            :loading="loadings.editCourse"
            :disabled="loadings.editCourse"
          >
            Submit
          </v-btn>
          <v-btn color="primary" @click="modifyCourseDialog = false">
            Cancel
          </v-btn>
        </span>
        <v-btn
          color="error"
          @click="deleteCourse"
          :loading="loadings.deleteCourse"
          :disabled="loadings.deleteCourse"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog v-model="showCoursesDialog" max-width="480px" scrollable>
    <v-card color="secondary">
      <v-card-title>Courses</v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-3" style="height: 450px">
        <v-card
          v-for="course in coursesOfUser"
          :key="course.id"
          variant="tonal"
          class="my-1"
          @click="showModifyCourseDialog(course.id)"
        >
          <v-card-text class="text-center">
            <b>{{ course.name }}</b>
            <br />
            Students: {{ course.students }}
          </v-card-text>
        </v-card>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn color="primary" @click="showCoursesDialog = false">
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog v-model="addProfessorDialog" max-width="480px">
    <v-card color="secondary">
      <v-card-title>New professor</v-card-title>
      <v-card-subtitle class="text-error"
        >New professor will have to verify his (her) email <br />
        even if you create him (her).</v-card-subtitle
      >
      <v-card-text class="pa-3">
        <v-form ref="addProfessorForm">
          <v-text-field
            v-model="newProfessor.email"
            label="Email"
            density="comfortable"
            :rules="[(v) => !!v || 'This field is required']"
          ></v-text-field>
          <v-text-field
            v-model="newProfessor.fullName"
            label="Full name"
            density="comfortable"
            :rules="[(v) => !!v || 'This field is required']"
          ></v-text-field>
          <v-text-field
            v-model="newProfessor.password"
            label="Password"
            density="comfortable"
            :append-inner-icon="!showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword ? 'text' : 'password'"
            :rules="[(v) => !!v || 'This field is required']"
            @click:append-inner="showPassword = !showPassword"
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions
        class="d-flex flex-row justify-space-between align-center"
      >
        <v-btn
          color="primary"
          @click="addProfessor"
          :loading="loadings.addProfessor"
          :disabled="loadings.addProfessor"
        >
          Submit
        </v-btn>
        <v-btn color="primary" @click="addProfessorDialog = false">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import MainHaeder from "@/components/MainHeader.vue";
import axios from "axios";
import { ref, reactive } from "@vue/reactivity";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { onMounted, watch } from "@vue/runtime-core";
const store = useStore();
const router = useRouter();
const modifyCourseDialog = ref(false);
const showCoursesDialog = ref(false);
const addProfessorDialog = ref(false);
const showPassword = ref(false);
const autoAnswering = ref(false);
const loadings = reactive({
  autoAnswering: false,
  getCourses: false,
  getProfessors: false,
  getStudents: false,
  editCourse: false,
  deleteCourse: false,
  addProfessor: false,
});
const coursesPanel = ref(undefined);
const courses = ref([]);
const searchCourses = ref("");
const professorsPanel = ref(undefined);
const professors = ref([]);
const searchProfessors = ref("");
const studentsPanel = ref(undefined);
const students = ref([]);
const searchStudents = ref("");

const coursesOfUser = ref([]);

const newProfessor = reactive({
  email: "",
  fullName: "",
  password: "",
});

const courseID = ref("");
const name = ref("");
const semester = ref("");
const selectedProfessor = ref(null);
const selectedStudents = ref([]);
const isCompleted = ref(false);
const editCourseForm = ref(null);
const addProfessorForm = ref(null);

const snackbar = reactive({
  isOpen: false,
  color: "",
  content: "",
});

watch(searchCourses, async (newValue, oldValue) => {
  oldValue;
  loadings.getCourses = true;
  await axios
    .get(`/admin/courses/?search=${newValue}`)
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
  loadings.getCourses = false;
});

watch(searchProfessors, async (newValue, oldValue) => {
  oldValue;
  loadings.getProfessors = true;
  await axios
    .get(`/admin/professors/?search=${newValue}`)
    .then((response) => {
      professors.value = response.data;
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
  loadings.getProfessors = false;
});

watch(searchStudents, async (newValue, oldValue) => {
  oldValue;
  loadings.getStudents = true;
  await axios
    .get(`/admin/students/?search=${newValue}`)
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
  loadings.getStudents = false;
});

onMounted(async () => {
  loadings.autoAnswering = true;
  await axios
    .get("/admin/auto_answer/")
    .then((response) => {
      autoAnswering.value = !response.data.is_off;
    })
    .catch((error) => {
      if (error.response && error.response.status === 401) {
        store.commit("initializeStore", {});
        router.push({ name: "login" });
      } else if (error.response && error.response.status === 403) {
        router.push({ name: "courses" });
      } else if (error.message) {
        snackbar.content = error.message;
        snackbar.color = "error";
        snackbar.isOpen = true;
      }
    });
  loadings.autoAnswering = false;
  loadings.getCourses = true;
  await axios
    .get("/admin/courses/")
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
  loadings.getCourses = false;
  loadings.getProfessors = true;
  await axios
    .get("/admin/professors/")
    .then((response) => {
      professors.value = response.data;
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
  loadings.getProfessors = false;
  loadings.getStudents = true;
  await axios
    .get("/admin/students/")
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
  loadings.getStudents = false;
});

async function getCourses() {
  searchCourses.value = "";
  if (coursesPanel.value === 0) {
    loadings.getCourses = true;
    await axios
      .get("/admin/courses/")
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
    loadings.getCourses = false;
  }
}

async function getProfessors() {
  searchProfessors.value = "";
  if (professorsPanel.value === 0) {
    loadings.getProfessors = true;
    await axios
      .get("/admin/professors/")
      .then((response) => {
        professors.value = response.data;
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
    loadings.getProfessors = false;
  }
}

async function getStudents() {
  searchStudents.value = "";
  if (studentsPanel.value === 0) {
    loadings.getStudents = true;
    await axios
      .get("/admin/students/")
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
    loadings.getStudents = false;
  }
}

async function showModifyCourseDialog(course) {
  searchStudents.value = "";
  searchProfessors.value = "";
  showCoursesDialog.value = false;
  loadings.getCourses = true;
  await axios
    .get(`/admin/course/${course}`)
    .then((response) => {
      courseID.value = response.data.id;
      name.value = response.data.name;
      semester.value = response.data.semester;
      selectedProfessor.value = response.data.professor;
      selectedStudents.value = response.data.students;
      isCompleted.value = response.data.is_completed;
      modifyCourseDialog.value = true;
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
  loadings.getCourses = false;
}

async function toggleAutoAnswering() {
  loadings.autoAnswering = true;
  await axios
    .post("/admin/auto_answer/")
    .then((response) => {
      autoAnswering.value = !response.data.is_off;
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
  loadings.autoAnswering = false;
}

async function editCourse() {
  const form = await editCourseForm.value.validate();
  if (form.valid) {
    loadings.editCourse = true;
    await axios
      .put(`/admin/course/${courseID.value}/`, {
        name: name.value,
        semester: semester.value,
        professor: selectedProfessor.value,
        students: selectedStudents.value,
        is_completed: isCompleted.value,
      })
      .then((response) => {
        let editedCourse = courses.value.filter(
          (c) => c.id === response.data.id
        );
        console.log(editedCourse);
        if (editedCourse.length > 0) {
          editedCourse[0].name = response.data.name;
          editedCourse[0].semester = response.data.semester;
          editedCourse[0].students = response.data.students.length;
        }
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
    modifyCourseDialog.value = false;
    loadings.editCourse = false;
  }
}

async function deleteCourse() {
  loadings.deleteCourse = true;
  await axios
    .delete(`/admin/course/${courseID.value}/`)
    .then((response) => {
      response;
      courses.value = courses.value.filter((c) => c.id !== courseID.value);
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
  modifyCourseDialog.value = false;
  loadings.deleteCourse = false;
}

async function showCourses(user) {
  coursesOfUser.value = [];
  await axios
    .get(`/admin/${user.role.toLowerCase()}/${user.id}/`)
    .then((response) => {
      coursesOfUser.value = response.data;
      showCoursesDialog.value = true;
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

async function addProfessor() {
  const form = await addProfessorForm.value.validate();
  if (form.valid) {
    loadings.addProfessor = true;
    await axios
      .post(`/auth/signup/`, {
        email: newProfessor.email,
        full_name: newProfessor.fullName,
        role: "PROFESSOR",
        password: newProfessor.password,
      })
      .then((response) => {
        let newProf = response.data;
        newProf["courses"] = 0;
        professors.value.unshift(newProf);
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
    addProfessorDialog.value = false;
    loadings.addProfessor = false;
  }
}

async function deleteUser(user) {
  await axios.delete(`/admin/user/${user.id}/`).then((response) => {
    response;
    if (user.role === "PROFESSOR") {
      professors.value = professors.value.filter((p) => p.id !== user.id);
    } else if (user.role === "STUDENT") {
      students.value = students.value.filter((s) => s.id !== user.id);
    }
  });
  showCoursesDialog.value = false;
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

.page-text {
  font-size: 20px;
  font-weight: 300;
  line-height: 75px;
  margin-top: 0 !important;
}

.main-blocks {
  background-color: #ffffff4d;
  border-radius: 20px;
  height: calc(100vh - 225px);
}
.main-blocks__items {
  max-height: calc(100vh - 315px);
  overflow: auto;
  .v-card {
    cursor: pointer;
    &:hover {
      background-color: #ddd;
    }
  }
}

.main-blocks,
.main-blocks__items {
  &::-webkit-scrollbar-track {
    background-color: #ffffff00;
    border-radius: 10px;
    border: none;
  }
}

.main-blocks,
.main-blocks__items {
  &::-webkit-scrollbar {
    width: 5px;
    background-color: #ffffff00;
  }
}

.main-blocks,
.main-blocks__items {
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    border: none;
    background-color: #ffffff00;
    background-image: -webkit-gradient(
      linear,
      40% 0%,
      75% 84%,
      from(#06534200),
      to(#06534200),
      color-stop(0.6, #aaa)
    );
  }
}

.user-delete-btn {
  position: absolute;
  bottom: 0;
  right: 0;
}
@media only screen and (max-width: 959px) {
  .main-blocks {
    height: auto;
    min-height: calc(calc(100vh - 225px) / 3);
  }
}
@media only screen and (max-width: 650px) {
  #container {
    margin-top: 80px;
    height: calc(100vh - 80px);
  }
}
</style>