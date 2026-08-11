
<template>
  <div>
   <div v-if="!trek" class="text-center py-5 text-muted">
    </div>

    <!-- selected Trek manage panel -->
    <div v-else>
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <div class="row align-items-center g-3">
            <div class="col-auto">
              <img :src="trek.image" class="rounded-3"
                   style="width:80px;height:70px;object-fit:cover"
                   @error="e=>e.target.src='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=80'" />
            </div>
            <div class="col">
              <h5 class="fw-bold mb-1">{{ trek.trek_name }}</h5>
              <div class="d-flex gap-3 flex-wrap text-muted small">
                <span><i class="bi bi-geo-alt me-1"></i>{{ trek.trek_Location }}</span>
                <span><i class="bi bi-calendar me-1"></i>{{ trek.start_date }} → {{ trek.end_date }}</span>
                <span><i class="bi bi-people me-1"></i>{{ filledSlots }} / {{ trek.total_slots }} booked</span>
                <span class="badge ms-1" :class="diffBadge(trek.trek_difficulty)">{{ trek.trek_difficulty }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Controls row -->
      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <label class="form-label fw-semibold small">Available Slots</label>
          <input type="number" class="form-control" v-model="form.avilable_Slots" min="0" />
        </div>
        <div class="col-md-3">
          <label class="form-label fw-semibold small">Trek Status</label>
          <select class="form-select" v-model="form.status">
            <option>Open</option>
            <option>Closed</option>
            <option>Upcoming</option>
          </select>
        </div>
        <div class="col-md-3 d-flex align-items-end">
          <button class="btn btn-primary w-100" :disabled="saving" @click="updateTrek">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            <i v-else class="bi bi-check2 me-1"></i>
            {{ saving ? 'Saving...' : 'Update Trek' }}
          </button>
        </div>
        <div class="col-md-3 d-flex align-items-end">
          <button class="btn w-100"
            :class="trek.completed ? 'btn-outline-success disabled' : 'btn-success'"
            :disabled="trek.completed"
            @click="markCompleted">
            <i class="bi bi-check2-all me-1"></i>
            {{ trek.completed ? '✓ Already Completed' : 'Mark as Completed' }}
          </button>
        </div>
      </div>

      <div v-if="msg" class="alert py-2 mb-3" :class="msgType==='success'?'alert-success':'alert-danger'">
        {{ msg }}
      </div>

      <!-- Participants table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom py-3">
          <h6 class="mb-0 fw-bold">
            <i class="bi bi-people me-2"></i>Participants ({{ participants.length }})
          </h6>
        </div>
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th class="ps-4 small text-secondary">#</th>
                <th class="small text-secondary">Name</th>
                <th class="small text-secondary">Email</th>
                <th class="small text-secondary">Contact</th>
                <th class="small text-secondary">Booked On</th>
                <th class="small text-secondary">Payment</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingP">
                <td colspan="6" class="text-center py-4">
                  <div class="spinner-border spinner-border-sm text-primary"></div>
                </td>
              </tr>
              <tr v-for="(p, i) in participants" :key="p.booking_id">
                <td class="ps-4 text-muted small">{{ i + 1 }}</td>
                <td class="fw-semibold small">{{ p.user_name }}</td>
                <td class="small text-muted">{{ p.email_id }}</td>
                <td class="small text-muted">{{ p.contact }}</td>
                <td class="small text-muted">{{ p.booking_date }}</td>
                <td>
                  <span class="badge"
                    :class="p.payment_status==='Paid'?'bg-success':'bg-warning text-dark'">
                    {{ p.payment_status }}
                  </span>
                </td>
              </tr>
              <tr v-if="!loadingP && participants.length === 0">
                <td colspan="6" class="text-center text-muted py-3">No participants yet</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://localhost:5000'

export default {
  name: 'StaffMyTreks',
  emits: ['go-tab'],

  // trek is passed from StaffDash.vue when user clicks Manage
  props: {
    trek: { type: Object, default: null }
  },

  data() {
    return {
      form:         { avilable_Slots: 0, status: 'Open' },
      participants: [],
      saving:       false,
      loadingP:     false,
      msg:          '',
      msgType:      'success'
    }
  },

  computed: {
    filledSlots() {
      if (!this.trek) return 0
      return Math.max(0, (this.trek.total_slots || 0) - (this.trek.avilable_Slots || 0))
    }
  },

  // When trek prop changes (user picks a different trek), reload form + participants
  watch: {
    trek(newTrek) {
      if (newTrek) {
        this.form = { avilable_Slots: newTrek.avilable_Slots, status: newTrek.status }
        this.loadParticipants(newTrek.trek_id)
      }
    }
  },

  mounted() {
    if (this.trek) {
      this.form = { avilable_Slots: this.trek.avilable_Slots, status: this.trek.status }
      this.loadParticipants(this.trek.trek_id)
    }
  },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    diffBadge(d) {
      return { Easy:'bg-success', Moderate:'bg-warning text-dark', Hard:'bg-danger', Expert:'bg-dark' }[d] || 'bg-secondary'
    },

    async loadParticipants(trekId) {
      this.loadingP    = true
      this.participants = []
      try {
        const r = await axios.get(`${API}/treks/${trekId}/participants`, { headers: this.authHeader() })
        this.participants = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loadingP = false }
    },

    async updateTrek() {
      this.saving = true; this.msg = ''
      try {
        await axios.put(`${API}/treks/${this.trek.trek_id}`, this.form, { headers: this.authHeader() })
        this.msg     = 'Trek updated successfully!'
        this.msgType = 'success'
        setTimeout(() => this.msg = '', 3000)
      } catch (e) {
        this.msg     = e.response?.data?.message || 'Update failed'
        this.msgType = 'danger'
      } finally { this.saving = false }
    },

    async markCompleted() {
      if (!confirm('Mark this trek as completed? This cannot be undone.')) return
      try {
        await axios.put(`${API}/treks/${this.trek.trek_id}`, {
          completed: true, status: 'Closed'
        }, { headers: this.authHeader() })
        this.trek.completed = true
        this.trek.status    = 'Closed'
        this.form.status    = 'Closed'
        this.msg     = 'Trek marked as completed!'
        this.msgType = 'success'
      } catch (e) {
        this.msg     = e.response?.data?.message || 'Error'
        this.msgType = 'danger'
      }
    }
  }
}
</script>
