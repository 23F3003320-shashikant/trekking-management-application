
<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom py-3">
          <h6 class="mb-0 fw-bold">
            <i class="bi bi-person-circle me-2"></i>My Profile
          </h6>
        </div>
        <div class="card-body">
          <div v-if="msg" class="alert py-2 small"
               :class="msgType==='success'?'alert-success':'alert-danger'">
            <i :class="msgType==='success'?'bi bi-check-circle-fill':'bi bi-exclamation-triangle-fill'"
               class="me-1"></i>
            {{ msg }}
          </div>

          <!-- Avatar -->
          <div class="text-center mb-4">
            <div class="rounded-circle bg-warning bg-opacity-10 d-inline-flex align-items-center justify-content-center mb-2"
                 style="width:64px;height:64px">
              <i class="bi bi-person-hiking fs-3 text-warning"></i>
            </div>
            <div class="badge bg-warning text-dark px-3 py-2 d-block mx-auto"
                 style="width:fit-content">
              Trekker
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold small">Full Name</label>
            <input class="form-control" v-model="profile.name" placeholder="Your full name" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold small">Email Address</label>
            <input class="form-control bg-light" v-model="profile.email_id" disabled />
            <div class="form-text">Email cannot be changed</div>
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold small">Contact Number</label>
            <input class="form-control" v-model="profile.contact" placeholder="Phone number" />
          </div>
          <div class="mb-4">
            <label class="form-label fw-semibold small">New Password</label>
            <input type="password" class="form-control" v-model="profile.password"
                   placeholder="Leave blank to keep current password" />
          </div>
          <button class="btn btn-primary w-100" :disabled="saving" @click="saveProfile">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            <i v-else class="bi bi-check2 me-1"></i>
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://localhost:5000'

export default {
  name: 'TrekkerProfile',

  data() {
    return {
      profile: { name:'', email_id:'', contact:'', password:'' },
      saving:  false,
      msg:     '',
      msgType: 'success'
    }
  },

  mounted() { this.fetchProfile() },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async fetchProfile() {
      try {
        const r = await axios.get(`${API}/profile`, { headers: this.authHeader() })
        this.profile = { ...r.data, password: '' }
      } catch (e) { console.error(e.message) }
    },

    async saveProfile() {
      this.saving = true
      this.msg    = ''
      try {
        await axios.put(`${API}/profile`, this.profile, { headers: this.authHeader() })
        localStorage.setItem('name', this.profile.name)
        this.profile.password = ''
        this.msg     = 'Profile updated successfully!'
        this.msgType = 'success'
        setTimeout(() => this.msg = '', 3000)
      } catch (e) {
        this.msg     = e.response?.data?.message || 'Update failed'
        this.msgType = 'danger'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
