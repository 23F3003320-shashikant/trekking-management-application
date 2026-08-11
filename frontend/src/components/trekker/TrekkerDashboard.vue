
<template>
  <div>
    <!-- Welcome heading -->
    <div class="mb-4">
      <h4 class="fw-bold text-dark mb-0">Welcome, {{ name }}! 👋</h4>
      <p class="text-muted small mb-0">
        Explore available treks and manage your bookings
      </p>
    </div>

    <!-- Stat cards -->
    <div class="row g-3 mb-4">
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3 py-3">
            <div class="p-2 rounded-3 bg-primary bg-opacity-10">
              <i class="bi bi-signpost-2 fs-4 text-primary"></i>
            </div>
            <div>
              <div class="fs-3 fw-bold">{{ openTreksCount }}</div>
              <div class="text-muted small">Open Treks</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3 py-3">
            <div class="p-2 rounded-3 bg-success bg-opacity-10">
              <i class="bi bi-journal-bookmark fs-4 text-success"></i>
            </div>
            <div>
              <div class="fs-3 fw-bold">{{ bookings.length }}</div>
              <div class="text-muted small">My Bookings</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3 py-3">
            <div class="p-2 rounded-3 bg-warning bg-opacity-10">
              <i class="bi bi-check2-circle fs-4 text-warning"></i>
            </div>
            <div>
              <div class="fs-3 fw-bold">{{ completedCount }}</div>
              <div class="text-muted small">Completed</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters row -->
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
      <h6 class="fw-bold mb-0">Available Treks</h6>
      <div class="d-flex gap-2 flex-wrap">
        <select class="form-select form-select-sm" v-model="filterDiff" style="width:155px">
          <option value="">Difficulty: All</option>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
          <option>Expert</option>
        </select>
        <select class="form-select form-select-sm" v-model="filterLoc" style="width:175px">
          <option value="">Location: All</option>
          <option v-for="l in locations" :key="l">{{ l }}</option>
        </select>
      </div>
    </div>

    <!-- Flash message -->
    <div v-if="flashMsg" class="alert py-2 mb-3 d-flex align-items-center gap-2"
         :class="flashType==='success'?'alert-success':'alert-danger'">
      <i :class="flashType==='success'?'bi bi-check-circle-fill':'bi bi-exclamation-triangle-fill'"></i>
      <span>{{ flashMsg }}</span>
    </div>

    <!-- Trek cards -->
    <div v-if="loadingTreks" class="text-center py-4">
      <div class="spinner-border spinner-border-sm text-primary me-2"></div>
      <span class="text-muted">Loading treks...</span>
    </div>

    <div v-else class="row g-3 mb-4">
      <div v-for="t in filteredTreks" :key="t.trek_id" class="col-md-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100 overflow-hidden trek-card">
          <div class="position-relative">
            <img :src="t.image" class="card-img-top"
                 style="height:170px;object-fit:cover"
                 @error="e=>e.target.src='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80'" />
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill shadow-sm"
                  :class="diffBadge(t.trek_difficulty)">{{ t.trek_difficulty }}</span>
            <span class="position-absolute top-0 start-0 m-2 badge rounded-pill shadow-sm"
                  :class="statusBadge(t.status)">{{ t.status }}</span>
          </div>
          <div class="card-body d-flex flex-column pb-3">
            <h6 class="fw-bold mb-1" style="font-size:0.95rem">{{ t.trek_name }}</h6>
            <p class="text-muted mb-2 small">
              <i class="bi bi-geo-alt me-1"></i>{{ t.trek_Location }}
            </p>
            <div class="d-flex gap-3 text-muted mb-2 small">
              <span><i class="bi bi-clock me-1"></i>{{ t.duration }} days</span>
              <span><i class="bi bi-people me-1"></i>{{ t.avilable_Slots }} slots</span>
            </div>
            <div class="text-muted mb-3 small">
              <i class="bi bi-calendar me-1"></i>{{ t.start_date }} — {{ t.end_date }}
            </div>
            <div class="mt-auto d-flex justify-content-between align-items-center">
              <span class="fw-bold text-primary">₹{{ (t.price || 0).toLocaleString() }}</span>
              <button class="btn btn-sm px-3 fw-semibold"
                :class="getBookBtnClass(t)"
                :disabled="isDisabled(t)"
                @click="bookTrek(t.trek_id)">
                <span v-if="bookingId === t.trek_id"
                      class="spinner-border spinner-border-sm me-1"></span>
                {{ getBookLabel(t) }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="filteredTreks.length === 0" class="col-12 text-center text-muted py-4">
        <i class="bi bi-search fs-1 d-block mb-2 opacity-50"></i>
        No open treks match your filters
      </div>
    </div>

    <!-- Mini bookings table -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center py-3">
        <h6 class="mb-0 fw-bold">My Recent Bookings</h6>
        <button class="btn btn-link btn-sm p-0 text-decoration-none"
                @click="$emit('go-tab', 'mybookings')">
          View All →
        </button>
      </div>
      <div v-if="loadingBookings" class="text-center py-3">
        <div class="spinner-border spinner-border-sm text-primary"></div>
      </div>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">Trek Name</th>
              <th class="small text-secondary">Booking Date</th>
              <th class="small text-secondary">Dates</th>
              <th class="small text-secondary">Status</th>
              <th class="small text-secondary">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings.slice(0, 3)" :key="b.booking_id">
              <td class="ps-4 fw-semibold small">{{ b.trek_name }}</td>
              <td class="small text-muted">{{ b.booking_date }}</td>
              <td class="small text-muted">{{ b.start_date }} – {{ b.end_date }}</td>
              <td>
                <span class="badge rounded-pill"
                  :class="b.status==='Confirmed'?'bg-success':'bg-danger'">
                  {{ b.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-danger py-0"
                        @click="cancelBooking(b.booking_id)">
                  Cancel
                </button>
              </td>
            </tr>
            <tr v-if="bookings.length === 0">
              <td colspan="5" class="text-center text-muted py-3 small">
                No bookings yet — book a trek above!
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
  name: 'TrekkerDashboard',
  emits: ['go-tab', 'bookings-changed'],

  data() {
    return {
      name:     localStorage.getItem('name') || 'Trekker',
      treks:    [],
      bookings: [],
      loadingTreks:    false,
      loadingBookings: false,
      filterDiff: '',
      filterLoc:  '',
      flashMsg:   '',
      flashType:  'success',
      bookingId:  null
    }
  },

  computed: {
    locations() {
      return [...new Set(this.treks.map(t => t.trek_Location))].sort()
    },
    openTreksCount() {
      return this.treks.filter(t => t.status === 'Open').length
    },
    completedCount() {
      return this.bookings.filter(b => b.completed === true).length
    },
    bookedIds() {
      return new Set(this.bookings.map(b => Number(b.trek_id)))
    },
    filteredTreks() {
      return this.treks.filter(t => {
        if (t.status !== 'Open') return false
        if (this.filterDiff && t.trek_difficulty !== this.filterDiff) return false
        if (this.filterLoc  && t.trek_Location   !== this.filterLoc)  return false
        return true
      })
    }
  },

  mounted() {
    this.fetchTreks()
    this.fetchBookings()
  },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    diffBadge(d) {
      return { Easy:'bg-success', Moderate:'bg-warning text-dark', Hard:'bg-danger', Expert:'bg-dark' }[d] || 'bg-secondary'
    },
    statusBadge(s) {
      return { Open:'bg-success', Closed:'bg-danger', Upcoming:'bg-info text-dark' }[s] || 'bg-secondary'
    },

    alreadyBooked(id) { return this.bookedIds.has(Number(id)) },

    isDisabled(t) {
      return (
        this.alreadyBooked(t.trek_id) ||
        t.status !== 'Open'           ||
        t.avilable_Slots <= 0         ||
        this.bookingId === t.trek_id
      )
    },

    getBookBtnClass(t) {
      if (this.alreadyBooked(t.trek_id))              return 'btn-outline-success'
      if (t.status !== 'Open' || t.avilable_Slots <= 0) return 'btn-secondary'
      return 'btn-primary'
    },

    getBookLabel(t) {
      if (this.bookingId === t.trek_id)    return 'Booking...'
      if (this.alreadyBooked(t.trek_id))  return '✓ Booked'
      if (t.status !== 'Open')             return t.status
      if (t.avilable_Slots <= 0)           return 'Full'
      return 'Book Now'
    },

    showFlash(msg, type = 'success') {
      this.flashMsg  = msg
      this.flashType = type
      clearTimeout(this._ft)
      this._ft = setTimeout(() => this.flashMsg = '', 4000)
    },

    async fetchTreks() {
      this.loadingTreks = true
      try {
        const r = await axios.get(`${API}/treks`)
        this.treks = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loadingTreks = false }
    },

    async fetchBookings() {
      this.loadingBookings = true
      try {
        const r = await axios.get(`${API}/bookings`, { headers: this.authHeader() })
        this.bookings = r.data.map(b => ({ ...b, trek_id: Number(b.trek_id) }))
        this.$emit('bookings-changed', new Set(this.bookings.map(b => b.trek_id)))
      } catch (e) { console.error(e.message) }
      finally { this.loadingBookings = false }
    },

    async bookTrek(trek_id) {
      const numId = Number(trek_id)
      if (this.alreadyBooked(numId)) return
      this.bookingId = numId
      try {
        const r = await axios.post(`${API}/bookings`, { trek_id: numId }, {
          headers: this.authHeader()
        })
        this.showFlash(`🎉 ${r.data.message} A confirmation email has been sent!`, 'success')
        await Promise.all([this.fetchTreks(), this.fetchBookings()])
        this.$emit('bookings-changed', new Set(this.bookings.map(b => b.trek_id)))
      } catch (e) {
        this.showFlash(e.response?.data?.message || 'Booking failed', 'danger')
      } finally {
        this.bookingId = null
      }
    },

    async cancelBooking(id) {
      if (!confirm('Cancel this booking?')) return
      try {
        await axios.delete(`${API}/bookings/${id}`, { headers: this.authHeader() })
        await Promise.all([this.fetchTreks(), this.fetchBookings()])
        this.showFlash('Booking cancelled. Cancellation email sent.', 'success')
      } catch (e) {
        this.showFlash(e.response?.data?.message || 'Cancel failed', 'danger')
      }
    }
  }
}
</script>

<style scoped>
.trek-card { transition: transform .2s, box-shadow .2s; }
.trek-card:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(0,0,0,0.12) !important; }
</style>
