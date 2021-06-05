import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/Home.vue"),
  },
  {
    path: "/posts/:id?",
    name: "posts",
    component: () => import("@/views/Posts.vue"),
  },
  {
    path: "/imprint",
    name: "imprint",
    component: () => import("@/views/Imprint.vue"),
  },
  {
    path: "/privacy",
    name: "privacy",
    component: () => import("@/views/Privacy.vue"),
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/About.vue"),
  },
  {
    path: "*",
    name: "not-found",
    component: () => import("@/views/PageNotFound.vue"),
  },
];

const router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

/** add route name as css class to body element */
router.beforeEach((to, from, next) => {
  const routeName = to.name || "";
  document.body.className = routeName;
  next();
});

export default router;
