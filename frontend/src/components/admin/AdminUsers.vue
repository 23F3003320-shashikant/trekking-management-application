
<template>
  <div>
    <div class="input-group mb-3" style="max-width:320px">
      <span class="input-group-text bg-white"><i class="bi bi-search text-muted"></i></span>
      <input class="form-control border-start-0" v-model="search" placeholder="Search by name or email..." />
    </div>

    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h6 class="mb-0 fw-bold">Trekkers — {{ filteredUsers.length }} total</h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">#</th>
              <th class="small text-secondary">Name</th>
              <th class="small text-secondary">Email</th>
              <th class="small text-secondary">Contact</th>
              <th class="small text-secondary">Joined</th>
              <th class="small text-secondary">Status</th>
              <th class="small text-secondary">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="7" class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary me-2"></div>Loading...
              </td>
            </tr>
            <tr v-for="(u, i) in filteredUsers" :key="u.email_id">
              <td class="ps-4 text-muted small">{{ i + 1 }}</td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="rounded-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center"
                       style="width:32px;height:32px;flex-shrink:0">
                    <i class="bi bi-person-fill text-primary" style="font-size:0.8rem"></i>
                  </div>
                  <span class="fw-semibold small">{{ u.name }}</span>
                </div>
              </td>
              <td class="small text-muted">{{ u.email_id }}</td>
              <td class="small text-muted">{{ u.contact }}</td>
              <td class="small text-muted">{{ u.created_at }}</td>
              <td>
                <span class="badge rounded-pill" :class="u.is_active ? 'bg-success' : 'bg-danger'">
                  {{ u.is_active ? 'Active' : 'Blacklisted' }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm me-1"
                  :class="u.is_active ? 'btn-outline-warning' : 'btn-outline-success'"
                  @click="toggleUser(u.email_id)">
                  <i :class="u.is_active ? 'bi bi-slash-circle' : 'bi bi-check-circle'" class="me-1"></i>
                  {{ u.is_active ? 'Blacklist' : 'Activate' }}
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteUser(u.email_id)">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>
            <tr v-if="!loading && filteredUsers.length === 0">
              <td colspan="7" class="text-center text-muted py-4">
                <i class="bi bi-people d-block fs-2 mb-2 opacity-50"></i>
                No users found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer bg-white py-2">
        <small class="text-muted">
          <i class="bi bi-info-circle me-1"></i>
          Blacklisted users cannot log in or book treks.
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://localhost:5000'

export default {
  name: 'AdminUsers',
  emits: ['refresh-stats'],

  data() {
    return {
      userList: [],
      loading:  false,
      search:   ''
    }
  },

  computed: {
    filteredUsers() {
      if (!this.search.trim()) return this.userList
      const q = this.search.toLowerCase()
      return this.userList.filter(u =>
        u.name.toLowerCase().includes(q) ||
        u.email_id.toLowerCase().includes(q)
      )
    }
  },

  mounted() { this.fetchUsers() },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async fetchUsers() {
      this.loading = true
      try {
        const r = await axios.get(`${API}/users`, { headers: this.authHeader() })
        this.userList = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    },

    async toggleUser(email) {
      try {
        await axios.put(`${API}/users/${email}/toggle`, {}, { headers: this.authHeader() })
        await this.fetchUsers()
      } catch (e) { alert(e.response?.data?.message || 'Error') }
    },

    async deleteUser(email) {
      if (!confirm('Delete this user? This cannot be undone.')) return
      try {
        await axios.delete(`${API}/users/${email}`, { headers: this.authHeader() })
        await this.fetchUsers()
        this.$emit('refresh-stats')
      } catch (e) { alert(e.response?.data?.message || 'Error') }
    }
  }
}
</script>
