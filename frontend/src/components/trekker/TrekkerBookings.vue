<template>
  <div>
    <!-- Booking summary cards -->
    <div class="row g-3 mb-4">
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3 py-3">
            <div class="p-2 rounded-3 bg-success bg-opacity-10">
              <i class="bi bi-journal-check fs-4 text-success"></i>
            </div>
            <div>
              <div class="fs-3 fw-bold">{{ confirmed }}</div>
              <div class="text-muted small">Confirmed</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3 py-3">
            <div class="p-2 rounded-3 bg-danger bg-opacity-10">
              <i class="bi bi-x-circle fs-4 text-danger"></i>
            </div>
            <div>
              <div class="fs-3 fw-bold">{{ cancelled }}</div>
              <div class="text-muted small">Cancelled</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3 py-3">
            <div class="p-2 rounded-3 bg-primary bg-opacity-10">
              <i class="bi bi-check2-all fs-4 text-primary"></i>
            </div>
            <div>
              <div class="fs-3 fw-bold">{{ completed }}</div>
              <div class="text-muted small">Completed</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Flash message -->
    <div v-if="msg" class="alert py-2 mb-3" :class="msgType==='success'?'alert-success':'alert-danger'">
      {{ msg }}
    </div>

    <!-- Bookings Table -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h6 class="mb-0 fw-bold">All My Bookings ({{ bookings.length }})</h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">#</th>
              <th class="small text-secondary">Trek</th>
              <th class="small text-secondary">Location</th>
              <th class="small text-secondary">Booked On</th>
              <th class="small text-secondary">Trek Dates</th>
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
            <tr v-for="b in bookings" :key="b.booking_id">
              <td class="ps-4 text-muted small">#{{ b.booking_id }}</td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <img :src="b.trek_image"
                       class="rounded" style="width:34px;height:34px;object-fit:cover"
                       @error="e=>e.target.src='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=60'" />
                  <span class="fw-semibold small">{{ b.trek_name }}</span>
                </div>
              </td>
              <td class="small text-muted">
                <i class="bi bi-geo-alt me-1"></i>{{ b.trek_location }}
              </td>
              <td class="small text-muted">{{ b.booking_date }}</td>
              <td class="small text-muted">{{ b.start_date }}<br>{{ b.end_date }}</td>
              <td>
                <span class="badge rounded-pill"
                  :class="b.status==='Confirmed'?'bg-success':'bg-danger'">
                  {{ b.status }}
                </span>
              </td>
              <td>
                <span class="badge"
                  :class="b.payment_status==='Paid'?'bg-success':'bg-warning text-dark'">
                  {{ b.payment_status }}
                </span>
              </td>
              <td>
                <button v-if="b.status==='Confirmed'"
                  class="btn btn-sm btn-outline-danger py-0"
                  @click="cancelBooking(b.booking_id)">
                  Cancel
                </button>
                <span v-else class="text-muted small">—</span>
              </td>
            </tr>
            <tr v-if="!loading && bookings.length === 0">
              <td colspan="8" class="text-center text-muted py-5">
                <i class="bi bi-journal-x fs-1 d-block mb-3 opacity-50"></i>
                <p class="mb-2">No bookings yet</p>
                <button class="btn btn-primary btn-sm" @click="$emit('go-browse')">
                  Browse Treks
                </button>
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
  name: 'TrekkerBookings',
  emits: ['bookings-loaded', 'go-browse'],

  data() {
    return {
      bookings: [],
      loading:  false,
      msg:      '',
      msgType:  'success'
    }
  },

  computed: {
    confirmed()  { return this.bookings.filter(b => b.status === 'Confirmed').length },
    cancelled()  { return this.bookings.filter(b => b.status === 'Cancelled').length },
    completed()  { return this.bookings.filter(b => b.completed === true).length }
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
        this.bookings = r.data.map(b => ({ ...b, trek_id: Number(b.trek_id) }))
        // Tell parent the latest bookedIds so Browse tab stays in sync
        this.$emit('bookings-loaded', new Set(this.bookings.map(b => b.trek_id)))
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    },

    async cancelBooking(id) {
      if (!confirm('Cancel this booking? A cancellation email will be sent to you.')) return
      try {
        await axios.delete(`${API}/bookings/${id}`, { headers: this.authHeader() })
        this.msg     = 'Booking cancelled. Check your email for confirmation.'
        this.msgType = 'success'
        await this.fetchBookings()
        setTimeout(() => this.msg = '', 4000)
      } catch (e) {
        this.msg     = e.response?.data?.message || 'Cancel failed'
        this.msgType = 'danger'
      }
    }
  }
}
</script>
