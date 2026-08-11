
<template>
  <div>
    <div class="mb-4">
      <h5 class="fw-bold text-dark mb-1">My Dashboard</h5>
      <p class="text-muted small mb-0">Welcome back, {{ name }}! Here are your assigned treks.</p>
    </div>

    <!-- Stat Cards -->
    <div class="row g-3 mb-4">
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-primary bg-opacity-10">
              <i class="bi bi-signpost-2 fs-4 text-primary"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ assignedTreks.length }}</div>
              <div class="text-muted small">Assigned Treks</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-success bg-opacity-10">
              <i class="bi bi-people fs-4 text-success"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ totalParticipants }}</div>
              <div class="text-muted small">Total Participants</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-warning bg-opacity-10">
              <i class="bi bi-check2-circle fs-4 text-warning"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ openTreks }}</div>
              <div class="text-muted small">Ongoing Treks</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Assigned Treks Table -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h6 class="mb-0 fw-bold">My Assigned Treks</h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">Trek Name</th>
              <th class="small text-secondary">Location</th>
              <th class="small text-secondary">Dates</th>
              <th class="small text-secondary">Participants</th>
              <th class="small text-secondary">Slots Left</th>
              <th class="small text-secondary">Status</th>
              <th class="small text-secondary">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="7" class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary me-2"></div>Loading...
              </td>
            </tr>
            <tr v-for="t in assignedTreks" :key="t.trek_id">
              <td class="ps-4">
                <div class="d-flex align-items-center gap-2">
                  <img :src="t.image" class="rounded" style="width:36px;height:36px;object-fit:cover"
                       @error="e=>e.target.src='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=60'" />
                  <span class="fw-semibold small">{{ t.trek_name }}</span>
                </div>
              </td>
              <td class="small text-muted"><i class="bi bi-geo-alt me-1"></i>{{ t.trek_Location }}</td>
              <td class="small text-muted">{{ t.start_date }}<br>{{ t.end_date }}</td>
              <td class="text-center">
                <span class="badge bg-primary bg-opacity-10 text-primary fw-semibold">
                  {{ Math.max(0, (t.total_slots || 0) - (t.avilable_Slots || 0)) }}
                </span>
              </td>
              <td class="small fw-semibold">{{ t.avilable_Slots }} / {{ t.total_slots }}</td>
              <td>
                <span class="badge rounded-pill" :class="statusBadge(t.status)">{{ t.status }}</span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-primary" @click="$emit('manage-trek', t)">
                  <i class="bi bi-pencil me-1"></i>Manage
                </button>
              </td>
            </tr>
            <tr v-if="!loading && assignedTreks.length === 0">
              <td colspan="7" class="text-center text-muted py-4">
                <i class="bi bi-signpost d-block fs-2 mb-2 opacity-50"></i>
                No treks assigned to you yet. Contact admin.
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
  name: 'StaffDashboard',
  emits: ['manage-trek'],

  data() {
    return {
      name:          localStorage.getItem('name') || 'Staff',
      myEmail:       localStorage.getItem('email_id') || '',
      assignedTreks: [],
      loading:       false
    }
  },

  computed: {
    totalParticipants() {
      return this.assignedTreks.reduce((sum, t) =>
        sum + Math.max(0, (t.total_slots || 0) - (t.avilable_Slots || 0)), 0)
    },
    openTreks() {
      return this.assignedTreks.filter(t => t.status === 'Open').length
    }
  },

  mounted() { this.fetchMyTreks() },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    statusBadge(s) {
      return { Open:'bg-success', Closed:'bg-danger', Upcoming:'bg-info text-dark' }[s] || 'bg-secondary'
    },

    async fetchMyTreks() {
      this.loading = true
      try {
        const [treksRes, staffRes] = await Promise.all([
          axios.get(`${API}/treks`),
          axios.get(`${API}/staff`, { headers: this.authHeader() })
        ])

        const me = staffRes.data.find(s => s.email_id === this.myEmail)
        if (me) {
          this.assignedTreks = treksRes.data.filter(t => t.assigned_staff_id === me.staff_id)
        } else {
          this.assignedTreks = []
        }
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    }
  }
}
</script>
