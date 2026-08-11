<template>
  <div>
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
        <h6 class="mb-0 fw-bold">All Bookings — {{ bookingList.length }} total</h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">ID</th>
              <th class="small text-secondary">Trekker</th>
              <th class="small text-secondary">Trek</th>
              <th class="small text-secondary">Location</th>
              <th class="small text-secondary">Booking Date</th>
              <th class="small text-secondary">Status</th>
              <th class="small text-secondary">Payment</th>
              <th class="small text-secondary">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="8" class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary me-2"></div>Loading...
              </td>
            </tr>
            <tr v-for="b in bookingList" :key="b.booking_id">
              <td class="ps-4 fw-semibold text-primary small">#{{ b.booking_id }}</td>
              <td class="small">{{ b.user_name }}</td>
              <td class="small fw-semibold">{{ b.trek_name }}</td>
              <td class="small text-muted">{{ b.trek_location }}</td>
              <td class="small text-muted">{{ b.booking_date }}</td>
              <td>
                <span class="badge rounded-pill"
                  :class="b.status === 'Confirmed' ? 'bg-success' : 'bg-danger'">
                  {{ b.status }}
                </span>
              </td>
              <td>
                <span class="badge"
                  :class="b.payment_status === 'Paid' ? 'bg-success' : 'bg-warning text-dark'">
                  {{ b.payment_status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-danger" @click="cancelBooking(b.booking_id)">
                  <i class="bi bi-x-circle me-1"></i>Cancel
                </button>
              </td>
            </tr>
            <tr v-if="!loading && bookingList.length === 0">
              <td colspan="8" class="text-center text-muted py-4">
                <i class="bi bi-journal-x d-block fs-2 mb-2 opacity-50"></i>No bookings yet
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
  name: 'AdminBookings',
  data() {
    return {
      bookingList: [],
      loading:     false
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
        this.bookingList = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    },

    async cancelBooking(id) {
      if (!confirm('Cancel this booking? A cancellation email will be sent to the trekker.')) return
      try {
        await axios.delete(`${API}/bookings/${id}`, { headers: this.authHeader() })
        await this.fetchBookings()
        this.$emit('refresh-stats')
      } catch (e) { alert(e.response?.data?.message || 'Error') }
    }
  }
}
</script>
