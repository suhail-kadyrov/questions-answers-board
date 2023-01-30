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
    <v-row class="ma-0">
      <v-col cols="3" class="hidden-sm-and-down pa-0 menu">
        <v-item-group selected-class="bg-primary">
          <v-item v-for="course in courses" :key="course.id">
            <router-link
              :to="{ name: 'course-detail', params: { id: course.id } }"
              class="courses-list__links"
            >
              <v-card
                class="
                  d-flex
                  align-center
                  bg-secondary
                  pa-2
                  my-1
                  courses-list__card
                "
              >
                <v-avatar
                  v-if="user.role === 'STUDENT'"
                  :image="course.professor.image"
                  size="50"
                  class="bg-primary mr-2"
                >
                  {{ getProfessorInitials(course.professor) }}
                </v-avatar>
                <div
                  class="flex-grow-1"
                  :class="{ 'text-center': user.role === 'PROFESSOR' }"
                >
                  <p :class="{ 'font-weight-bold': user.role === 'PROFESSOR' }">
                    {{ course.name }}
                  </p>
                  <p v-if="user.role === 'STUDENT'" class="font-weight-bold">
                    {{ course.professor.full_name }}
                  </p>
                  <p v-else>Students: {{ course.students }}</p>
                </div>
              </v-card>
            </router-link>
          </v-item>
        </v-item-group>
      </v-col>
      <v-col cols="12" md="9" class="py-0 chat">
        <div>
          <p
            v-if="course"
            class="ma-1 page-text d-flex align-center justify-space-between"
          >
            <span>{{ course.name }}</span>
            <span>
              <v-btn
                v-if="user.role === 'PROFESSOR'"
                prepend-icon="mdi-account-multiple-plus"
                color="secondary"
                variant="tonal"
              >
                Invite students
                <v-dialog
                  v-model="dialogInvite"
                  activator="parent"
                  max-width="480px"
                >
                  <v-card color="secondary">
                    <v-card-title>{{ course.name }}</v-card-title>
                    <v-card-text class="pa-3">
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
                    </v-card-text>
                    <v-card-actions
                      class="d-flex flex-row justify-space-between align-center"
                    >
                      <v-btn
                        color="primary"
                        @click="inviteStudents"
                        :loading="loadings.inviteStudents"
                        :disabled="loadings.inviteStudents"
                      >
                        Submit
                      </v-btn>
                      <v-btn color="primary" @click="dialogInvite = false">
                        Cancel
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-btn>
              <v-icon
                v-if="course.is_completed"
                icon="mdi-check-circle"
                size="x-small"
                color="success"
              ></v-icon>
              <v-icon
                v-else
                icon="mdi-clock"
                size="x-small"
                color="warning"
              ></v-icon>
            </span>
          </p>
          <v-expansion-panels
            :class="{ 'thread-list-prof': user.role === 'PROFESSOR' }"
            v-model="currentThread"
            @update:modelValue="getMessages"
          >
            <v-expansion-panel
              v-for="thread in threads"
              :key="thread.id"
              class="bg-secondary my-1"
            >
              <v-expansion-panel-title class="medium-text">
                <span
                  v-if="store.getters.getUser.role === 'PROFESSOR'"
                  class="d-flex flex-column align-center mr-4"
                >
                  <v-avatar
                    :image="thread.student.image"
                    size="30"
                    class="bg-primary"
                  >
                    {{ getStudentInitials(thread.student) }}
                  </v-avatar>
                  <span class="text-caption">{{
                    thread.student.full_name.split(" ")[0]
                  }}</span>
                </span>
                {{ thread.title }}
                <v-badge
                  v-if="
                    store.state.notifications
                      .filter((n) => !n.is_seen)
                      .filter(
                        (n) =>
                          n.name === 'STUDENT_NEW_ANSWER' ||
                          n.name === 'PROFESSOR_NEW_QUESTION'
                      )
                      .filter((n) => n.message.thread === thread.id).length > 0
                  "
                  dot
                  inline
                  color="error"
                ></v-badge>
                <v-progress-circular
                  v-if="
                    thread.id === getCurrentThread(currentThread)?.id &&
                    loadings.getMessages
                  "
                  color="primary"
                  :size="20"
                  :width="2"
                  class="ml-3"
                  indeterminate
                ></v-progress-circular>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="medium-text">
                <div class="chat-bubbles__wrapper" @scroll="scrDB">
                  <p
                    v-for="message in messages"
                    :id="`message${message.id}`"
                    :key="message.id"
                    class="d-flex"
                    :class="{
                      'flex-row-reverse': message.sender.role === user.role,
                    }"
                  >
                    <v-badge
                      v-if="
                        store.state.notifications
                          .filter((n) => !n.is_seen)
                          .filter(
                            (n) =>
                              n.name === 'STUDENT_NEW_ANSWER' ||
                              n.name === 'PROFESSOR_NEW_QUESTION'
                          )
                          .filter((n) => n.message.id === message.id).length > 0
                      "
                      dot
                      inline
                      color="error"
                    ></v-badge>
                    <span
                      class="text-left chat__bubble"
                      :class="{
                        'text-other': message.sender.role !== user.role,
                        'text-me': message.sender.role === user.role,
                      }"
                    >
                      <a
                        v-if="message.reply_to_message"
                        :href="`#message${message.reply_to_message.id}`"
                        class="chat__reply text-truncate"
                        @click="highlightReply(message.reply_to_message.id)"
                      >
                        <b>{{ message.reply_to_message.sender.full_name }}</b>
                        <br />
                        {{ message.reply_to_message.text }}
                      </a>
                      {{ message.text }}
                      <span class="d-block chat__timestamp text-right">
                        <span v-if="true">
                          <v-icon
                            v-if="message.is_edited"
                            size="sm"
                            icon="mdi-pencil"
                          ></v-icon>
                        </span>
                        {{
                          new Date(message.sent_at).toLocaleString("en-GB", {
                            timeZone:
                              Intl.DateTimeFormat().resolvedOptions().timeZone,
                          })
                        }}
                      </span>
                    </span>
                    <span class="d-flex flex-column-reverse pb-2 align-end">
                      <v-btn
                        v-if="
                          message.sender.role === user.role &&
                          (user.role !== 'STUDENT' ||
                            (course && !course.is_completed))
                        "
                        size="x-small"
                        color="error"
                        variant="tonal"
                        icon
                        @click="confirmDelete(message)"
                      >
                        <v-icon icon="mdi-delete"></v-icon>
                      </v-btn>
                      <v-btn
                        v-if="
                          message.sender.role === user.role &&
                          (user.role !== 'STUDENT' ||
                            (course && !course.is_completed))
                        "
                        size="x-small"
                        color="info"
                        variant="tonal"
                        icon
                        @click="confirmEdit(message)"
                      >
                        <v-icon icon="mdi-pencil"></v-icon>
                      </v-btn>
                      <v-btn
                        v-if="message.sender.role !== user.role"
                        size="x-small"
                        color="primary"
                        variant="tonal"
                        icon="mdi-reply"
                        @click="doReply(message)"
                      >
                      </v-btn>
                    </span>
                  </p>
                  <v-btn
                    icon="mdi-chevron-down"
                    class="chat__down-arrow"
                    size="x-small"
                    color="primary"
                    variant="tonal"
                    @click="scrollBottom"
                  ></v-btn>
                </div>
                <div class="mt-2">
                  <div
                    v-if="reply.id"
                    class="d-flex align-center justify-space-between mb-2"
                  >
                    <a
                      :href="`#message${reply.id}`"
                      class="chat__reply text-truncate ma-0"
                      @click="highlightReply(reply.id)"
                    >
                      <b>{{ reply.sender.full_name }}</b>
                      <br />
                      {{ reply.text }}
                    </a>
                    <v-icon
                      icon="mdi-close"
                      class="undo-reply"
                      @click="undoReply"
                    ></v-icon>
                  </div>
                  <div class="d-flex flex-row align-center">
                    <v-combobox
                      v-if="
                        user.role === 'STUDENT' &&
                        course &&
                        !course.is_completed
                      "
                      v-model="newMessageText"
                      hide-details
                      variant="outlined"
                      label="Write your question ..."
                      class="medium-text"
                      :items="recommendedQuestions"
                      item-title="question"
                      item-value="question"
                      :custom-filter="customFilter"
                      :menu-props="{ theme: 'dark' }"
                      :rules="[(v) => !!v || 'Message is required!']"
                    ></v-combobox>
                    <v-text-field
                      v-else-if="user.role === 'PROFESSOR'"
                      v-model="newMessageText"
                      hint="Reply to a question, if you want to save your answer"
                      variant="outlined"
                      label="Write your answer ..."
                      class="medium-text"
                      :rules="[(v) => !!v || 'Message is required!']"
                    >
                    </v-text-field>
                    <v-btn
                      v-if="
                        user.role !== 'STUDENT' ||
                        (course && !course.is_completed)
                      "
                      icon="mdi-send"
                      variant="text"
                      :loading="loadings.sendMessage"
                      :disabled="loadings.sendMessage"
                      @click="sendMessage"
                    ></v-btn>
                  </div>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
          <div class="text-center">
            <v-progress-circular
              v-if="loadings.getThreads"
              color="secondary"
              :size="100"
              :width="2"
              class="ml-3"
              indeterminate
            ></v-progress-circular>
          </div>
        </div>
        <div
          v-if="user.role === 'STUDENT' && course && !course.is_completed"
          class="d-flex flex-row align-center"
        >
          <v-combobox
            v-model="newThreadText"
            hide-details
            variant="outlined"
            label="Start new thread ..."
            class="medium-text"
            :items="recommendedQuestions"
            item-title="question"
            item-value="question"
            :custom-filter="customFilter"
            :menu-props="{ theme: 'dark' }"
            :rules="[(v) => !!v || 'Message is required!']"
          ></v-combobox>
          <v-btn
            icon="mdi-send"
            variant="text"
            @click="sendNewThread"
            :loading="loadings.sendThread"
            :disabled="loadings.sendThread"
          ></v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <v-dialog
    v-model="dialogEdit"
    persistent
    transition="dialog-top-transition"
    max-width="480px"
  >
    <v-card class="custom-dialog-box">
      <v-card-text class="pa-3">
        <v-combobox
          v-model="editMessageText"
          variant="outlined"
          label="Edit message"
          class="medium-text"
          :items="recommendedQuestions"
          item-title="question"
          item-value="question"
          :custom-filter="customFilter"
          :menu-props="{ theme: 'dark' }"
          :rules="[(v) => !!v || 'Message is required!']"
        ></v-combobox>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="dialogEdit = false">Cancel</v-btn>
        <v-btn
          color="primary"
          @click="editMessage"
          :loading="loadings.editMessage"
          :disabled="loadings.editMessage"
          >Submit</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog
    v-model="dialogDelete"
    persistent
    transition="dialog-top-transition"
    max-width="480px"
  >
    <v-card class="custom-dialog-box">
      <v-card-text> Are you sure you want to delete the message? </v-card-text>
      <v-card-actions>
        <v-btn
          color="error"
          @click="deleteMessage"
          :loading="loadings.deleteMessage"
          :disabled="loadings.deleteMessage"
          >Delete</v-btn
        >
        <v-btn color="primary" @click="dialogDelete = false"> Cancel </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import MainHaeder from "@/components/MainHeader.vue";
import axios from "axios";
import { onMounted, reactive, ref, computed, watch } from "vue";
import { onBeforeRouteUpdate, useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import ws from "@/services/ws";
const store = useStore();
const route = useRoute();
const router = useRouter();
const courses = ref([]);
const course = ref(null);
const currentThread = ref(undefined);
const threads = ref([]);
const messages = ref([]);
const newThreadText = ref(null);
const newMessageText = ref(null);
const editMessageText = ref(null);
const recommendedQuestions = ref([]);

const students = ref([]);
const selectedStudents = ref([]);

const loadings = reactive({
  getMessages: false,
  getThreads: false,
  sendMessage: false,
  sendThread: false,
  deleteMessage: false,
  editMessage: false,
  inviteStudents: false,
});

const snackbar = reactive({
  isOpen: false,
  color: "",
  content: "",
});

const user = computed(() => store.getters.getUser);

const dialogDelete = ref(false);
const modifyMessageID = ref(null);
const dialogEdit = ref(false);
const dialogInvite = ref(false);

const reply = reactive({
  id: null,
  text: null,
  sender: null,
});

async function recommendQuestions(query) {
  await axios
    .get(`/question/?course_id=${course.value.id}&search=${query}`)
    .then((response) => {
      recommendedQuestions.value = response.data;
    });
}
watch(newThreadText, async (newValue, oldValue) => {
  oldValue;
  await recommendQuestions(newValue);
});

watch(newMessageText, async (newValue, oldValue) => {
  oldValue;
  await recommendQuestions(newValue);
});

watch(editMessageText, async (newValue, oldValue) => {
  oldValue;
  await recommendQuestions(newValue);
});

async function wsOnMessage(e) {
  const data = JSON.parse(e.data);
  if (
    data.type === "MESSAGE" &&
    data.data.thread === getCurrentThread(currentThread.value)?.id
  ) {
    messages.value.push(data.data);
    setTimeout(scrollBottom, 1);
  } else if (
    data.type === "EDITED_MESSAGE" &&
    data.data.thread === getCurrentThread(currentThread.value)?.id
  ) {
    let editedMsg = messages.value.filter((m) => m.id === data.data.id);
    if (editedMsg.length > 0) {
      editedMsg[0].is_edited = true;
      editedMsg[0].text = data.data.text;
    }
  } else if (data.type === "DELETED_MESSAGE") {
    await axios
      .get(`/chat/thread/${getCurrentThread(currentThread.value)?.id}/`)
      .then((response) => {
        messages.value = response.data;
      })
      .catch((error) => {
        if (error.response && error.response.status === 401) {
          store.commit("initializeStore", {});
          router.push({ name: "login" });
        }
      });
  } else if (data.type === "THREAD") {
    threads.value.unshift(data.data);
    document.querySelector(".chat>div").scrollTop = 0;
    currentThread.value = undefined;
  }
}

onMounted(async () => {
  ws.addEventListener("message", wsOnMessage);
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
    .get(`/course/${route.params.id}`)
    .then((response) => {
      threads.value = response.data.threads;
      course.value = response.data.course;
    })
    .catch((error) => {
      if (error.response && error.response.status === 404) {
        snackbar.content = "Course is not found!";
        snackbar.color = "error";
        snackbar.isOpen = true;
        setTimeout(() => {
          router.push({ name: "courses" });
        }, 2000);
      } else if (error.response && error.response.status === 401) {
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

onBeforeRouteUpdate(async (to, from) => {
  if (to.name === "course-detail" && to.params.id !== from.params.id) {
    currentThread.value = undefined;
    threads.value = [];
    loadings.getThreads = true;
    await axios
      .get(`/course/${to.params.id}`)
      .then((response) => {
        threads.value = response.data.threads;
        course.value = response.data.course;
      })
      .catch((error) => {
        if (error.response && error.response.status === 404) {
          snackbar.content = "Course is not found!";
          snackbar.color = "error";
          snackbar.isOpen = true;
          setTimeout(() => {
            router.push({ name: "courses" });
          }, 2000);
        } else if (error.response && error.response.status === 401) {
          store.commit("initializeStore", {});
          router.push({ name: "login" });
        } else if (error.message) {
          snackbar.content = error.message;
          snackbar.color = "error";
          snackbar.isOpen = true;
        }
      });
    loadings.getThreads = false;
  } else if (to.name !== "course-detail") {
    ws.removeEventListener("message", wsOnMessage);
  }
});

async function getMessages(event) {
  messages.value = [];
  loadings.getMessages = true;
  if (typeof event === "undefined") return;
  const threadID = getCurrentThread(event).id;
  await axios
    .get(`/chat/thread/${threadID}/`)
    .then((response) => {
      messages.value = response.data;
      loadings.getMessages = false;
      setTimeout(scrollBottom, 1);
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

function doReply(message) {
  reply["id"] = message.id;
  reply["sender"] = message.sender;
  reply["text"] = message.text;
}

function undoReply() {
  reply["id"] = null;
  delete reply["sender"];
  delete reply["text"];
}

function scrollBottom() {
  const msgs = document.getElementsByClassName("chat-bubbles__wrapper")[0];
  if (msgs) {
    let shouldScroll = msgs.scrollTop + msgs.clientHeight >= msgs.scrollHeight;
    if (!shouldScroll) {
      msgs.scrollTop = msgs.scrollHeight;
    }
  }
}

async function sendMessage() {
  if (typeof currentThread.value === "undefined") return;
  if (!newMessageText.value) return;
  const threadID = getCurrentThread(currentThread.value).id;
  loadings.sendMessage = true;
  let formData = {
    thread: threadID,
    text:
      typeof newMessageText.value === "string"
        ? newMessageText.value
        : newMessageText.value.question,
    reply_to_message: reply.id,
  };
  await axios
    .post("/chat/message/", formData)
    .then((response) => {
      messages.value.push(response.data.data);
      setTimeout(scrollBottom, 1);
      newMessageText.value = null;
      undoReply();
      loadings.sendMessage = false;
      if (response.data.answer) {
        setTimeout(() => {
          messages.value.push(response.data.answer);
          setTimeout(scrollBottom, 1);
        }, 300);
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
}

async function sendNewThread() {
  if (!newThreadText.value) return;
  loadings.sendThread = true;
  let formData = {
    course: course.value.id,
    text:
      typeof newThreadText.value === "string"
        ? newThreadText.value
        : newThreadText.value.question,
  };
  await axios
    .post("/chat/thread/", formData)
    .then((response) => {
      threads.value.unshift(response.data);
      document.querySelector(".chat>div").scrollTop = 0;
      newThreadText.value = null;
      loadings.sendThread = false;
      currentThread.value = undefined;
    })
    .catch((error) => {
      console.log(error);
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

function confirmDelete(msg) {
  dialogDelete.value = true;
  modifyMessageID.value = msg.id;
}

function confirmEdit(msg) {
  dialogEdit.value = true;
  modifyMessageID.value = msg.id;
  editMessageText.value = msg.text;
}

async function deleteMessage() {
  if (modifyMessageID.value) {
    loadings.deleteMessage = true;
    await axios
      .delete(`/chat/message/${modifyMessageID.value}/`)
      .then((response) => {
        response;
        messages.value = messages.value.filter(
          (m) => m.id !== modifyMessageID.value
        );
        dialogDelete.value = false;
        modifyMessageID.value = null;
      });
    loadings.deleteMessage = false;
  }
}

async function editMessage() {
  if (modifyMessageID.value) {
    loadings.editMessage = true;
    await axios
      .put(`/chat/message/${modifyMessageID.value}/`, {
        text:
          typeof editMessageText.value === "string"
            ? editMessageText.value
            : editMessageText.value.question,
      })
      .then((response) => {
        let editedMsg = messages.value.filter(
          (m) => m.id === modifyMessageID.value
        );
        if (editedMsg.length > 0) {
          editedMsg[0].is_edited = true;
          editedMsg[0].text = response.data.data.text;
        }

        if (response.data.answer) {
          setTimeout(() => {
            messages.value.push(response.data.answer);
            setTimeout(scrollBottom, 1);
          }, 300);
        }

        dialogEdit.value = false;
        modifyMessageID.value = null;
      });
    loadings.editMessage = false;
  }
}

async function inviteStudents() {
  loadings.inviteStudents = true;
  await axios.patch(`/course/${course.value.id}/`, {
    students: selectedStudents.value,
  });
  loadings.inviteStudents = false;
  selectedStudents.value = [];
  dialogInvite.value = false;
}

function scrDB() {
  const msgs = document.getElementsByClassName("chat-bubbles__wrapper")[0];
  const scb = document.getElementsByClassName("chat__down-arrow")[0];
  scb.style.bottom = `-${msgs.scrollTop}px`;

  if (msgs.scrollHeight == msgs.scrollTop + msgs.clientHeight) {
    scb.style.display = "none";
  } else {
    scb.style.display = "inline";
  }
}

function highlightReply(id) {
  let elem = document.querySelector("#message" + id);
  elem.style.backgroundColor = "#06534222";
  elem.style.borderRadius = "10px";
  setTimeout(() => {
    elem.style.backgroundColor = "#ffffff00";
  }, 1000);
}

function getProfessorInitials(professor) {
  return professor.full_name
    .trim()
    .split(" ")
    .map((name) => name[0])
    .join("")
    .toUpperCase();
}

function getCurrentThread(threadIndex) {
  return threads.value[threadIndex];
}

function customFilter(value, query, item) {
  item;
  return true;
}

function getStudentInitials(student) {
  return student.full_name
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
  scrollbar-color: #06534299 #ebf6f2;
  scrollbar-width: thin !important;
}

#container,
.menu,
.chat-bubbles__wrapper,
.chat > div > div {
  &::-webkit-scrollbar-track {
    background-color: #ffffff00;
    border-radius: 10px;
    border: none;
  }
}

#container,
.menu,
.chat-bubbles__wrapper,
.chat > div > div {
  &::-webkit-scrollbar {
    width: 3px;
    background-color: #ffffff00;
  }
}

#container,
.menu,
.chat-bubbles__wrapper,
.chat > div > div {
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    border: none;
    background-color: #ffffff00;
    background-image: -webkit-gradient(
      linear,
      40% 0%,
      75% 84%,
      from(#06534222),
      to(#06534222),
      color-stop(0.6, #ebf6f2)
    );
  }
}
.page-text {
  font-size: 54px;
  font-weight: 300;
  line-height: 75px;
  margin-top: 0 !important;
}
.menu {
  height: calc(100vh - 145px);
  overflow-x: hidden;
  overflow-y: auto;
}
.chat {
  height: calc(100vh - 145px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  > div:nth-child(1) > div:nth-child(2) {
    max-height: calc(100vh - 290px);
    scroll-behavior: smooth;
    overflow-y: auto;
    &.thread-list-prof {
      max-height: calc(100vh - 225px);
    }
  }
}
.chat-bubbles__wrapper {
  max-height: calc(100vh - 480px);
  overflow-y: auto;
  scroll-behavior: smooth;
  position: relative;
}
.chat__down-arrow {
  position: absolute;
  right: 0;
  bottom: 0;
}
.chat__bubble {
  display: inline-block;
  max-width: 85%;
  margin: 5px 0;
  padding: 10px;
  &.text- {
    &other {
      color: #065342;
      background-color: #0653424d;
      border-radius: 20px 20px 20px 0px;
    }
    &me {
      color: #002b59;
      background-color: #002b594d;
      border-radius: 20px 20px 0px 20px;
    }
  }
}
.chat__timestamp {
  font-size: 12px;
}
.chat__reply {
  display: block;
  font-size: 12px;
  border-left: 2px solid black;
  margin-bottom: 10px;
  padding-left: 5px;
  cursor: pointer;
  border-radius: 5px;
  text-decoration: none;
  color: inherit;
  &:hover {
    background-color: #06534222;
  }
}
.undo-reply {
  color: #777;
  cursor: pointer;
  &:hover {
    color: black;
  }
}
.courses-list__links {
  text-decoration: none;
  font-size: 24px;
  p {
    line-height: 24px;
  }
}
.courses-list__card {
  border-radius: 20px;
  transition: 0.2s;
  &:hover {
    transform: scale(0.88);
  }
}
.router-link-exact-active .courses-list__card {
  transform: scale(0.88);
}
.custom-dialog-box {
  background-color: #fbf7f5;
  color: #002b59;
}
@media only screen and (max-width: 650px) {
  #container {
    margin-top: 80px;
    height: calc(100vh - 80px);
  }
  .page-text {
    font-size: 48px;
    font-weight: 300;
    line-height: 75px;
    margin-top: 0 !important;
  }
  .chat {
    padding: 0;
  }
}
</style>