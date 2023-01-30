import { createRouter, createWebHistory } from "vue-router";
import store from '../store'
import LoginView from "../views/authentication/LoginView.vue";
import SignupView from "../views/authentication/SignupView.vue";
import VerifiedView from "../views/authentication/VerifiedView.vue";
import PasswordResetView from "../views/authentication/PasswordResetView.vue";
import PasswordResetDoneView from "../views/authentication/PasswordResetDoneView.vue";
import PasswordResetCompleteView from "../views/authentication/PasswordResetCompleteView.vue";
import CoursesView from "../views/courses/CoursesView.vue";
import ExploreView from "../views/courses/ExploreView.vue";
import CourseDetailView from "../views/courses/CourseDetailView.vue";
import AccountView from "../views/AccountView.vue";
import DashboardView from "../views/admin/DashboardView.vue";
import Error404View from "../views/Error404View.vue";

const routes = [
  {
    path: '',
    redirect: '/admin'
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignupView,
  },
  {
    path: "/verified",
    name: "verified",
    component: VerifiedView,
  },
  {
    path: "/reset-password",
    name: "reset-password",
    component: PasswordResetView,
  },
  {
    path: "/reset-password-done",
    name: "reset-password-done",
    component: PasswordResetDoneView,
  },
  {
    path: "/reset-password-complete",
    name: "reset-password-complete",
    component: PasswordResetCompleteView,
  },
  {
    path: "/account",
    name: "account",
    component: AccountView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/courses",
    name: "courses",
    component: CoursesView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/courses/explore",
    name: "explore",
    component: ExploreView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/courses/:id",
    name: "course-detail",
    component: CourseDetailView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: "/admin",
    name: "admin-dashboard",
    component: DashboardView,
    meta: {
      requireLogin: true,
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'error-404',
    component: Error404View
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(path => path.meta.requireLogin) && !store.getters.getIsAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router;
