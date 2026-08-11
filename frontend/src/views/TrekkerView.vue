<template>
  <div>
    <TrekkerDash v-if="isLoggedIn" />
    <LoginPage v-else />
  </div>
</template>
<script>
import LoginPage from '../components/LoginPage.vue'
import TrekkerDash from '../components/TrekkerDash.vue'
export default {
  components: { LoginPage, TrekkerDash },
  computed: { isLoggedIn() { return localStorage.getItem('token') && localStorage.getItem('role') === 'trekker' } }
}
</script>
