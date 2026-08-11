
<template>
  <div>
    <!-- Top bar -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="input-group" style="max-width:280px">
        <span class="input-group-text bg-white"><i class="bi bi-search text-muted"></i></span>
        <input class="form-control border-start-0" v-model="search" placeholder="Search staff..." />
      </div>
      <button class="btn btn-primary" @click="openForm">
        <i class="bi bi-plus-lg me-1"></i>Create New Staff
      </button>
    </div>

    <!-- ── CREATE STAFF FORM ── -->
    <div v-if="showForm" class="card border-primary border-2 shadow mb-4">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h6 class="mb-0 fw-bold"><i class="bi bi-person-plus me-2"></i>Create New Trekking Staff</h6>
        <button class="btn-close btn-close-white" @click="closeForm"></button>
      </div>
      <div class="card-body">
        <div v-if="formMsg" class="alert py-2 mb-3" :class="formMsgType==='success'?'alert-success':'alert-danger'">
          {{ formMsg }}
        </div>
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Full Name *</label>
            <input class="form-control" v-model="form.staff_name" placeholder="e.g. Rohit Singh" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Email Address *</label>
            <input type="email" class="form-control" v-model="form.email_id" placeholder="staff@email.com" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Contact Number *</label>
            <input class="form-control" v-model="form.contact" placeholder="e.g. 9876543210" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Password</label>
            <input type="password" class="form-control" v-model="form.password" placeholder="Default: staff123" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Specialization</label>
            <input class="form-control" v-model="form.specialization" placeholder="e.g. High Altitude, First Aid" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Experience</label>
            <input class="form-control" v-model="form.experience" placeholder="e.g. 3 years" />
          </div>
        </div>
        <div class="alert alert-info d-flex gap-2 align-items-start mt-3 mb-0 py-2">
          <i class="bi bi-envelope-fill flex-shrink-0 mt-1 text-info"></i>
          <small>Login credentials will be emailed to the staff via MailHog. Check <strong>http://localhost:8025</strong></small>
        </div>
      </div>
      <div class="card-footer bg-white d-flex gap-2 justify-content-end">
        <button class="btn btn-light" @click="closeForm">Cancel</button>
        <button class="btn btn-success px-4" :disabled="saving" @click="createStaff">
          <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
          {{ saving ? 'Creating...' : 'Create Staff' }}
        </button>
      </div>
    </div>

    <!-- ── Staff Table ── -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h6 class="mb-0 fw-bold">Trekking Staff List</h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">#</th>
              <th class="small text-secondary">Name</th>
              <th class="small text-secondary">Email</th>
              <th class="small text-secondary">Contact</th>
              <th class="small text-secondary">Specialization</th>
              <th class="small text-secondary">Experience</th>
              <th class="small text-secondary">Status</th>
              <th class="small text-secondary">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="8" class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary me-2"></div>Loading...
              </td>
            </tr>
            <tr v-for="s in filteredStaff" :key="s.staff_id">
              <td class="ps-4 text-muted small">{{ s.staff_id }}</td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="rounded-circle bg-success bg-opacity-10 d-flex align-items-center justify-content-center"
                       style="width:34px;height:34px;flex-shrink:0">
                    <i class="bi bi-person-fill text-success small"></i>
                  </div>
                  <span class="fw-semibold small">{{ s.staff_name }}</span>
                </div>
              </td>
              <td class="small text-muted">{{ s.email_id }}</td>
              <td class="small text-muted">{{ s.contact }}</td>
              <td class="small text-muted">{{ s.specialization || '—' }}</td>
              <td class="small text-muted">{{ s.experience || '—' }}</td>
              <td>
                <span class="badge rounded-pill" :class="s.is_active ? 'bg-success' : 'bg-danger'">
                  {{ s.is_active ? 'Active' : 'Blacklisted' }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm me-1"
                  :class="s.is_active ? 'btn-outline-warning' : 'btn-outline-success'"
                  @click="toggleStaff(s.staff_id)"
                  :title="s.is_active ? 'Blacklist' : 'Activate'">
                  <i :class="s.is_active ? 'bi bi-slash-circle' : 'bi bi-check-circle'"></i>
                  {{ s.is_active ? 'Blacklist' : 'Activate' }}
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteStaff(s.staff_id)" title="Delete">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>
            <tr v-if="!loading && filteredStaff.length === 0">
              <td colspan="8" class="text-center text-muted py-4">
                <i class="bi bi-person-x d-block fs-2 mb-2 opacity-50"></i>
                No staff found. Blacklisted staff cannot log in.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://localhost:5000'

export default {
  name: 'AdminStaff',
  emits: ['refresh-stats', 'staff-updated'],

  data() {
    return {
      staffList: [],
      loading:   false,
      search:    '',

      showForm:    false,
      saving:      false,
      formMsg:     '',
      formMsgType: 'success',
      form: {
        staff_name:'', email_id:'', contact:'',
        password:'', specialization:'', experience:''
      }
    }
  },

  computed: {
    filteredStaff() {
      if (!this.search.trim()) return this.staffList
      const q = this.search.toLowerCase()
      return this.staffList.filter(s =>
        s.staff_name.toLowerCase().includes(q) ||
        s.email_id.toLowerCase().includes(q)
      )
    }
  },

  mounted() { this.fetchStaff() },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async fetchStaff() {
      this.loading = true
      try {
        const r = await axios.get(`${API}/staff`, { headers: this.authHeader() })
        this.staffList = r.data
        // Tell parent to update its staffList too (used in trek assignment dropdown)
        this.$emit('staff-updated', r.data)
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    },

    openForm() {
      this.formMsg = ''
      this.form    = { staff_name:'', email_id:'', contact:'', password:'', specialization:'', experience:'' }
      this.showForm = true
    },

    closeForm() {
      this.showForm = false
      this.formMsg  = ''
    },

    async createStaff() {
      // Validate required fields
      if (!this.form.staff_name.trim()) { this.formMsg='Name is required';    this.formMsgType='danger'; return }
      if (!this.form.email_id.trim())   { this.formMsg='Email is required';   this.formMsgType='danger'; return }
      if (!this.form.contact.trim())    { this.formMsg='Contact is required'; this.formMsgType='danger'; return }

      if (!this.form.password.trim()) this.form.password = 'staff123'

      this.saving = true; this.formMsg = ''
      try {
        const r = await axios.post(`${API}/staff`, this.form, { headers: this.authHeader() })
        this.formMsg     = `✅ Staff "${this.form.staff_name}" created! Login email sent to ${this.form.email_id}`
        this.formMsgType = 'success'
        this.form        = { staff_name:'', email_id:'', contact:'', password:'', specialization:'', experience:'' }
        await this.fetchStaff()
        this.$emit('refresh-stats')
        setTimeout(() => { this.showForm = false; this.formMsg = '' }, 3500)
      } catch (e) {
        this.formMsg     = e.response?.data?.message || 'Failed to create staff'
        this.formMsgType = 'danger'
      } finally { this.saving = false }
    },

    async toggleStaff(id) {
      try {
        await axios.put(`${API}/staff/${id}/toggle`, {}, { headers: this.authHeader() })
        await this.fetchStaff()
      } catch (e) { alert(e.response?.data?.message || 'Error') }
    },

    async deleteStaff(id) {
      if (!confirm('Remove this staff member?')) return
      try {
        await axios.delete(`${API}/staff/${id}`, { headers: this.authHeader() })
        await this.fetchStaff()
        this.$emit('refresh-stats')
      } catch (e) { alert(e.response?.data?.message || 'Error') }
    }
  }
}
</script>
