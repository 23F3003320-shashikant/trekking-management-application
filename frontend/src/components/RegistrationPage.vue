<template>
  <div class="auth-bg d-flex align-items-center justify-content-center min-vh-100">
    <div class="auth-card card shadow-lg border-0 p-0 overflow-hidden" style="width:860px;max-width:96vw">
      <div class="row g-0">

        <!-- Left panel -->
        <div class="col-md-5 d-flex flex-column justify-content-between reg-left position-relative">
          <div class="reg-overlay"></div>
          <div class="p-5 position-relative" style="z-index:2">
            <div class="d-flex align-items-center gap-2 mb-4">
              <div class="brand-icon rounded-circle d-flex align-items-center justify-content-center">
                <i class="bi bi-mountains-fill fs-5 text-white"></i>
              </div>
              <div>
                <div class="fw-bold text-white lh-1" style="font-size:0.95rem">Trekking Management</div>
                <div class="text-white-50" style="font-size:0.7rem">Application</div>
              </div>
            </div>
            <h3 class="text-white fw-bold mb-2">Create Account</h3>
            <p class="text-white-50">Register as a Trekker</p>
          </div>
        </div>

        <!-- Right panel: form -->
        <div class="col-md-7 bg-white d-flex flex-column justify-content-center p-5">
          <h4 class="fw-bold mb-1">Create Your Account</h4>
          <p class="text-muted small mb-4">Fill in your details to get started</p>

          <div v-if="errorMsg" class="alert alert-danger d-flex gap-2 py-2 align-items-center">
            <i class="bi bi-exclamation-triangle-fill flex-shrink-0"></i>
            <span class="small">{{ errorMsg }}</span>
          </div>
          <div v-if="successMsg" class="alert alert-success d-flex gap-2 py-2 align-items-center">
            <i class="bi bi-check-circle-fill flex-shrink-0"></i>
            <span class="small">{{ successMsg }}</span>
          </div>

          <form @submit.prevent="doRegister">
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary">Full Name *</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0">
                  <i class="bi bi-person text-muted"></i>
                </span>
                <input type="text" class="form-control bg-light border-start-0"
                       v-model="form.name" placeholder="Your full name" required />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary">Email Address *</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0">
                  <i class="bi bi-envelope text-muted"></i>
                </span>
                <input type="email" class="form-control bg-light border-start-0"
                       v-model="form.email_id" placeholder="your@email.com" required />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary">Password *</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0">
                  <i class="bi bi-lock text-muted"></i>
                </span>
                <input type="password" class="form-control bg-light border-start-0"
                       v-model="form.password" placeholder="Choose a password" required />
              </div>
            </div>
            <div class="mb-4">
              <label class="form-label small fw-semibold text-secondary">Contact Number *</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0">
                  <i class="bi bi-phone text-muted"></i>
                </span>
                <input type="tel" class="form-control bg-light border-start-0"
                       v-model="form.contact" placeholder="Phone number" required />
              </div>
            </div>
            <button type="submit" class="btn btn-success w-100 fw-semibold py-2"
                    :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Registering...' : 'Register as Trekker' }}
            </button>
          </form>

          <div class="text-center mt-4">
            <span class="text-muted small">Already have an account? </span>
            <button class="btn btn-link btn-sm p-0 fw-semibold text-primary text-decoration-none"
                    @click="$emit('show-login')">
              Login here
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegistrationPage',
  emits: ['show-login'],

  data() {
    return {
      form:       { name:'', email_id:'', password:'', contact:'' },
      errorMsg:   '',
      successMsg: '',
      loading:    false
    }
  },

  methods: {
    async doRegister() {
      this.errorMsg   = ''
      this.successMsg = ''
      this.loading    = true
      try {
        await axios.post('http://localhost:5000/register', this.form)
        this.successMsg = '✅ Registered! ...'
        // login after just register
        const r = await axios.post('http://localhost:5000/login', {
          email_id: this.form.email_id,
          password: this.form.password
        })
        const { access_token, role, name, email_id } = r.data
        localStorage.setItem('token',    access_token)
        localStorage.setItem('role',     role)
        localStorage.setItem('name',     name)
        localStorage.setItem('email_id', email_id)
        setTimeout(() => this.$router.push('/trekker'), 1500)
      } catch (e) {
        this.errorMsg = e.response?.data?.message || 'Registration failed. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-bg { background: linear-gradient(135deg,#0f2027,#203a43,#2c5364); }
.auth-card { border-radius:16px !important; }
.reg-left {
  background: url('https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&q=80') center/cover no-repeat;
  min-height: 200px;
}
.reg-overlay { position:absolute;inset:0;background:linear-gradient(160deg,rgba(15,32,39,0.82),rgba(44,83,100,0.75)); }
.brand-icon { width:38px;height:38px;background:linear-gradient(135deg,#6366f1,#3b82f6); }
.input-group-text { border-color:#e9ecef !important; }
.form-control { border-color:#e9ecef !important; }
.form-control:focus { box-shadow:none; border-color:#198754 !important; }
.text-white-75 { color:rgba(255,255,255,0.75) !important; }
</style>
