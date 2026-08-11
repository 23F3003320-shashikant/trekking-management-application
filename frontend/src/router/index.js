import { createRouter, createWebHistory } from "vue-router"
import HomePage    from "../views/HomePage.vue"
import AdminView   from "../views/AdminView.vue"
import StaffView   from "../views/StaffView.vue"
import TrekkerView from "../views/TrekkerView.vue"

const routes = [
  { path: '/',         component: HomePage    },
  { path: '/admin',    component: AdminView   },
  { path: '/staff',    component: StaffView   },
  { path: '/trekker',  component: TrekkerView },
  { path: '/:pathMatch(.*)*', redirect: '/'  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
