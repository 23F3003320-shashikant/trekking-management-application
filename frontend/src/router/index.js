import AdminView from "../views/AdminView.vue"
import HomePage from "../views/HomePage.vue"
import StaffView from "../views/StaffView.vue"
import TrekkerView from "../views/TrekkerView.vue"

import { createRouter, createWebHistory} from "vue-router"

const routes = [
  { path: '/', component: HomePage},
  { path: '/admin', component: AdminView},
  { path: '/staff', component: StaffView},
  { path: '/trekker', component: TrekkerView},
  { path:  '/:pathMatch(.*)*', redirect: '/'}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router