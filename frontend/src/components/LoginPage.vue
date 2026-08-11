<template>
  <div class="auth-bg d-flex align-items-center justify-content-center min-vh-100">
    <div class="auth-card card shadow-lg border-0 p-0 overflow-hidden" style="width:860px;max-width:96vw">
      <div class="row g-0">

        <!-- Left panel -->
        <div class="col-md-5 auth-left d-flex flex-column justify-content-between p-5">
          <div>
            <div class="d-flex align-items-center gap-2 mb-4">
              <div class="brand-icon rounded-circle d-flex align-items-center justify-content-center">
                <i class="bi bi-mountains-fill fs-5 text-white"></i>
              </div>
              <div>
                <div class="fw-bold text-white lh-1" style="font-size:0.95rem">Trekking Management</div>
                <div class="text-white-50" style="font-size:0.7rem">Application</div>
              </div>
            </div>
            <h3 class="text-white fw-bold mb-1">Welcome Back!</h3>
            <p class="text-white-30 fw-bold mb-4">Login to your account</p>
          </div>
        </div>

        <!-- Right panel -->
        <div class="col-md-7 bg-white d-flex flex-column justify-content-center p-5">
          <h4 class="fw-bold mb-1 text-dark">Sign In</h4>
          <div v-if="errorMsg" class="alert alert-danger d-flex gap-2 py-2 align-items-center">
            <i class="bi bi-exclamation-triangle-fill flex-shrink-0"></i>
            <span class="small">{{ errorMsg }}</span>
          </div>

          <form @submit.prevent="doLogin">
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary">Email address</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0"><i class="bi bi-envelope text-muted"></i></span>
                <input type="email" class="form-control bg-light border-start-0" v-model="form.email_id" placeholder="Enter email" required />
              </div>
            </div>
            <div class="mb-4">
              <label class="form-label small fw-semibold text-secondary">Password</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0"><i class="bi bi-lock text-muted"></i></span>
                <input :type="showPwd ? 'text' : 'password'" class="form-control bg-light border-start-0 border-end-0" v-model="form.password" placeholder="Enter password" required />
                <button type="button" class="input-group-text bg-light border-start-0" @click="showPwd = !showPwd">
                  <i :class="`bi ${showPwd ? 'bi-eye-slash' : 'bi-eye'} text-muted`"></i>
                </button>
              </div>
            </div>
            <button type="submit" class="btn btn-primary w-100 fw-semibold py-2" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Signing in...' : 'Login' }}
            </button>
          </form>

          <div class="text-center mt-3">
            <span class="text-muted small">Don't have an account? </span>
            <a href="/register" class="fw-semibold text-primary text-decoration-none" @click.prevent="goRegister">Register as Trekker</a>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default{
  name:'LoginPage',
  data() {
  return{
    form: {
      eamil_id:'',
      password:'',
    },
    errorMsg:'',
    loading: false,
    showPwd:false,
    }
  },
  methods: {
    fillCred(c) { this.form.email_id = c.email; this.form.password = c.pass },
    goRegister() { this.$router.push('/') },
    async doLogin() {
      this.errorMsg = ''; this.loading = true
      try {
        const r = await axios.post('http://localhost:5000/login', this.form)
        const { access_token, role, name, email_id } = r.data
        localStorage.setItem('token',    access_token)
        localStorage.setItem('role',     role)
        localStorage.setItem('name',     name)
        localStorage.setItem('email_id', email_id)
        if (role === 'admin') {this.$router.push('/admin')}
        else if (role === 'staff') { this.$router.push('/staff')}
        else {  this.$router.push('/trekker')}
      } catch (e) {
        this.errorMsg = e.response?.data?.message || 'Login failed. Check credentials.'
      } finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.auth-bg { background: linear-gradient(135deg,#0f2027,#203a43,#2c5364); }
.auth-card { border-radius:14px !important; }
.auth-left { background: linear-gradient(160deg,#4352d9,#0d1f3c); min-height:px; }
.brand-icon { width:38px;height:38px;background:linear-gradient(135deg,#6366f1,#3b82f6); }
.input-group-text { border-color:#e9ecef !important; }
.form-control { border-color:#e9ecef !important; }
.form-control:focus { box-shadow:none; border-color:#3f82e6 !important; }
</style>
