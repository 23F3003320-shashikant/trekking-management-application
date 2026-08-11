<template>
  <div>
    <AdminDash v-if="isLoggedIn" />
    <LoginPage v-else />
  </div>
</template>
<script>
import LoginPage from '../components/admin/AdminDashboard.vue'
import AdminDash from '@/components/AdminDash.vue';
export default {
  components: {  LoginPage, AdminDash},
  computed: { isLoggedIn() { return localStorage.getItem('token') && localStorage.getItem('role') === 'admin' } }
}
</script>
