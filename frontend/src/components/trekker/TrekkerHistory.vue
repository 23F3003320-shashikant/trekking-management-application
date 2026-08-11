
<template>
  <div>
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h6 class="mb-0 fw-bold">
          <i class="bi bi-clock-history me-2"></i>Trekking History
        </h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">Trek Name</th>
              <th class="small text-secondary">Location</th>
              <th class="small text-secondary">Trek Dates</th>
              <th class="small text-secondary">Completed On</th>
              <th class="small text-secondary">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary me-2"></div>Loading...
              </td>
            </tr>
            <tr v-for="b in completedBookings" :key="b.booking_id">
              <td class="ps-4 fw-semibold small">{{ b.trek_name }}</td>
              <td class="small text-muted">
                <i class="bi bi-geo-alt me-1"></i>{{ b.trek_location }}
              </td>
              <td class="small text-muted">{{ b.start_date }} – {{ b.end_date }}</td>
              <td class="small text-muted">{{ b.completed_on || '—' }}</td>
              <td>
                <span class="badge bg-success rounded-pill">
                  <i class="bi bi-check2 me-1"></i>Completed
                </span>
              </td>
            </tr>
            <tr v-if="!loading && completedBookings.length === 0">
              <td colspan="5" class="text-center text-muted py-5">
                <i class="bi bi-clock-history fs-1 d-block mb-3 opacity-50"></i>
                <p class="mb-0 small">No completed treks yet. Keep trekking!</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer bg-white py-2">
        <small class="text-muted">
          <i class="bi bi-info-circle me-1"></i>
          History shows all your completed treks.
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://localhost:5000'

export default {
  name: 'TrekkerHistory',

  data() {
    return {
      allBookings: [],
      loading:     false
    }
  },

  computed: {
    completedBookings() {
      return this.allBookings.filter(b => b.completed === true)
    }
  },

  mounted() { this.fetchBookings() },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async fetchBookings() {
      this.loading = true
      try {
        const r = await axios.get(`${API}/bookings`, { headers: this.authHeader() })
        this.allBookings = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    }
  }
}
</script>
