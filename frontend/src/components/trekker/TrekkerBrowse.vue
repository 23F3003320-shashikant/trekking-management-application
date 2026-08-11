
<template>
  <div>
    <!-- Search bar -->
    <div class="row g-3 mb-4 align-items-end">
      <div class="col-md-4">
        <label class="form-label fw-semibold small">Search</label>
        <div class="input-group">
          <span class="input-group-text bg-white border-end-0">
            <i class="bi bi-search text-muted"></i>
          </span>
          <input class="form-control border-start-0" v-model="searchQ"
                 placeholder="Trek name or location..." />
        </div>
      </div>
      <div class="col-md-3">
        <label class="form-label fw-semibold small">Difficulty</label>
        <select class="form-select" v-model="filterDiff">
          <option value="">All Difficulties</option>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
          <option>Expert</option>
        </select>
      </div>
      <div class="col-md-3">
        <label class="form-label fw-semibold small">Location</label>
        <select class="form-select" v-model="filterLoc">
          <option value="">All Locations</option>
          <option v-for="l in locations" :key="l">{{ l }}</option>
        </select>
      </div>
      <div class="col-md-2">
        <button class="btn btn-outline-secondary w-100" @click="clearFilters">
          <i class="bi bi-x-circle me-1"></i>Clear
        </button>
      </div>
    </div>

    <!-- Flash message -->
    <div v-if="flashMsg" class="alert py-2 mb-3 d-flex align-items-center gap-2"
         :class="flashType==='success'?'alert-success':'alert-danger'">
      <i :class="flashType==='success'?'bi bi-check-circle-fill':'bi bi-exclamation-triangle-fill'"></i>
      <span>{{ flashMsg }}</span>
      <button class="btn-close ms-auto py-1" style="font-size:0.7rem" @click="flashMsg=''"></button>
    </div>

    <!-- Trek count -->
    <p class="text-muted small mb-3">
      Showing <strong>{{ filteredTreks.length }}</strong> trek{{ filteredTreks.length !== 1 ? 's' : '' }}
    </p>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-3 text-muted">Loading treks...</p>
    </div>

    <!-- Trek Cards Grid -->
    <div v-else class="row g-4">
      <div v-for="t in filteredTreks" :key="t.trek_id" class="col-md-6 col-xl-4">
        <div class="card border-0 shadow-sm h-100 overflow-hidden trek-card">
          <div class="position-relative">
            <img :src="t.image" class="card-img-top"
                 style="height:200px;object-fit:cover"
                 @error="e=>e.target.src='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80'" />
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill shadow-sm"
                  :class="diffBadge(t.trek_difficulty)">{{ t.trek_difficulty }}</span>
            <span class="position-absolute bottom-0 start-0 m-2 badge rounded-pill shadow-sm"
                  :class="statusBadge(t.status)">{{ t.status }}</span>
            <!-- Already booked indicator -->
            <div v-if="alreadyBooked(t.trek_id)"
                 class="position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
                 style="background:rgba(0,0,0,0.25);pointer-events:none">
              <span class="badge bg-success fs-6 shadow px-3 py-2">
                <i class="bi bi-check-circle-fill me-1"></i>Booked
              </span>
            </div>
          </div>
          <div class="card-body d-flex flex-column">
            <h6 class="fw-bold mb-1">{{ t.trek_name }}</h6>
            <p class="text-muted small mb-2">
              <i class="bi bi-geo-alt me-1"></i>{{ t.trek_Location }}
            </p>
            <p class="small text-muted mb-3 lh-sm"
               style="display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">
              {{ t.description }}
            </p>
            <div class="row g-1 text-muted small mb-3">
              <div class="col-6">
                <i class="bi bi-clock me-1 text-primary"></i>{{ t.duration }} days
              </div>
              <div class="col-6">
                <i class="bi bi-people me-1 text-primary"></i>{{ t.avilable_Slots }} slots left
              </div>
              <div class="col-12 mt-1">
                <i class="bi bi-calendar me-1 text-primary"></i>{{ t.start_date }} — {{ t.end_date }}
              </div>
            </div>
            <div class="mt-auto d-flex justify-content-between align-items-center">
              <span class="fw-bold text-primary fs-6">₹{{ (t.price || 0).toLocaleString() }}</span>
              <button class="btn btn-sm px-4 fw-semibold"
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

    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://localhost:5000'

export default {
  name: 'TrekkerBrowse',

  // bookedIds is a Set of trek_ids already booked by this user
  props: {
    bookedIds: { type: Object, default: () => new Set() }
  },

  emits: ['booking-changed'],

  data() {
    return {
      treks:    [],
      loading:  false,
      searchQ:  '',
      filterDiff: '',
      filterLoc:  '',
      flashMsg:   '',
      flashType:  'success',
      bookingId:  null    // which trek is currently being booked
    }
  },

  computed: {
    locations() {
      return [...new Set(this.treks.map(t => t.trek_Location))].sort()
    },
    filteredTreks() {
      const q = this.searchQ.trim().toLowerCase()
      return this.treks.filter(t => {
        if (q && !t.trek_name.toLowerCase().includes(q) &&
                 !t.trek_Location.toLowerCase().includes(q)) return false
        if (this.filterDiff && t.trek_difficulty !== this.filterDiff) return false
        if (this.filterLoc  && t.trek_Location  !== this.filterLoc)  return false
        return true
      })
    }
  },

  mounted() { this.fetchTreks() },

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

    alreadyBooked(id) {
      return this.bookedIds.has(Number(id))
    },

    isDisabled(t) {
      return (
        this.alreadyBooked(t.trek_id) ||
        t.status !== 'Open'           ||
        t.avilable_Slots <= 0         ||
        this.bookingId === t.trek_id
      )
    },

    getBookBtnClass(t) {
      if (this.alreadyBooked(t.trek_id)) return 'btn-outline-success'
      if (t.status !== 'Open' || t.avilable_Slots <= 0) return 'btn-secondary'
      return 'btn-primary'
    },

    getBookLabel(t) {
      if (this.bookingId === t.trek_id) return 'Booking...'
      if (this.alreadyBooked(t.trek_id)) return '✓ Booked'
      if (t.status !== 'Open') return t.status
      if (t.avilable_Slots <= 0) return 'Full'
      return 'Book Now'
    },

    clearFilters() {
      this.searchQ    = ''
      this.filterDiff = ''
      this.filterLoc  = ''
    },

    showFlash(msg, type = 'success') {
      this.flashMsg  = msg
      this.flashType = type
      clearTimeout(this._ft)
      this._ft = setTimeout(() => this.flashMsg = '', 4000)
    },

    async fetchTreks() {
      this.loading = true
      try {
        const r = await axios.get(`${API}/treks`)
        this.treks = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
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
        // Tell parent to refresh bookings so bookedIds updates
        this.$emit('booking-changed')
        await this.fetchTreks()    // refresh slots
      } catch (e) {
        this.showFlash(e.response?.data?.message || 'Booking failed', 'danger')
      } finally {
        this.bookingId = null
      }
    }
  }
}
</script>

<style scoped>
.trek-card { transition: transform .2s, box-shadow .2s; }
.trek-card:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(0,0,0,0.12) !important; }
</style>
