<template>
  <div>
    <StaffDash v-if="isLoggedIn" />
    <LoginPage v-else />
  </div>
</template>
<script>
import LoginPage from '../components/LoginPage.vue'
import StaffDash from '../components/StaffDash.vue'
export default {
  components: { LoginPage, StaffDash },
  computed: { isLoggedIn() { return localStorage.getItem('token') && localStorage.getItem('role') === 'staff' } }
}
</script>
