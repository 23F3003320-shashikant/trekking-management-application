
<template>
  <div>
    <!-- Top bar -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="input-group" style="max-width:280px">
        <span class="input-group-text bg-white"><i class="bi bi-search text-muted"></i></span>
        <input class="form-control border-start-0" v-model="search" placeholder="Search treks..." />
      </div>
      <button class="btn btn-primary" @click="openAddForm">
        <i class="bi bi-plus-lg me-1"></i>Add New Trek
      </button>
    </div>

    <!-- Success/Error message -->
    <div v-if="msg" class="alert py-2 mb-3" :class="msgType === 'success' ? 'alert-success' : 'alert-danger'">
      {{ msg }}
    </div>

    <!-- ── ADD / EDIT TREK FORM ── -->
    <div v-if="showForm" class="card border-primary border-2 shadow mb-4">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h6 class="mb-0 fw-bold">
          <i class="bi bi-signpost-2 me-2"></i>{{ editId ? 'Edit Trek' : 'Add New Trek' }}
        </h6>
        <button class="btn-close btn-close-white" @click="closeForm"></button>
      </div>
      <div class="card-body">
        <div v-if="formMsg" class="alert py-2 mb-3" :class="formMsgType==='success'?'alert-success':'alert-danger'">
          {{ formMsg }}
        </div>
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Trek Name *</label>
            <input class="form-control" v-model="form.trek_name" placeholder="e.g. Everest Base Camp" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Location *</label>
            <input class="form-control" v-model="form.trek_Location" placeholder="e.g. Nepal" />
          </div>
          <div class="col-md-4">
            <label class="form-label fw-semibold small">Difficulty</label>
            <select class="form-select" v-model="form.trek_difficulty">
              <option>Easy</option>
              <option>Moderate</option>
              <option>Hard</option>
              <option>Expert</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label fw-semibold small">Start Date *</label>
            <input type="date" class="form-control" v-model="form.start_date" />
          </div>
          <div class="col-md-4">
            <label class="form-label fw-semibold small">End Date *</label>
            <input type="date" class="form-control" v-model="form.end_date" />
          </div>
          <div class="col-md-4">
            <label class="form-label fw-semibold small">Duration (days)</label>
            <input type="number" class="form-control" v-model="form.duration" min="1" />
          </div>
          <div class="col-md-4">
            <label class="form-label fw-semibold small">Total Slots</label>
            <input type="number" class="form-control" v-model="form.avilable_Slots" min="1" />
          </div>
          <div class="col-md-4">
            <label class="form-label fw-semibold small">Price (₹)</label>
            <input type="number" class="form-control" v-model="form.price" min="0" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Assign Staff</label>
            <select class="form-select" v-model="form.assigned_staff_id">
              <option :value="null">— Not assigned —</option>
              <option v-for="s in staffList" :key="s.staff_id" :value="s.staff_id">
                {{ s.staff_name }}
              </option>
            </select>
          </div>
          <div class="col-md-6">
            <label class="form-label fw-semibold small">Status</label>
            <select class="form-select" v-model="form.status">
              <option>Open</option>
              <option>Closed</option>
              <option>Upcoming</option>
            </select>
          </div>
          <div class="col-12">
            <label class="form-label fw-semibold small">Image URL (leave blank for auto)</label>
            <input class="form-control" v-model="form.image" placeholder="https://..." />
          </div>
          <div class="col-12">
            <label class="form-label fw-semibold small">Description</label>
            <textarea class="form-control" v-model="form.description" rows="3"
              placeholder="Short description of the trek"></textarea>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white d-flex gap-2 justify-content-end">
        <button class="btn btn-light" @click="closeForm">Cancel</button>
        <button class="btn btn-primary px-4" :disabled="saving" @click="saveTrek">
          <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
          {{ saving ? 'Saving...' : (editId ? 'Update Trek' : 'Add Trek') }}
        </button>
      </div>
    </div>

    <!-- ── Participants panel ── -->
    <div v-if="showParticipants && currentTrek" class="card border-info border-2 shadow mb-4">
      <div class="card-header bg-info text-white d-flex justify-content-between">
        <h6 class="mb-0 fw-bold">
          <i class="bi bi-people me-2"></i>{{ currentTrek.trek_name }} — Participants ({{ participants.length }})
        </h6>
        <button class="btn-close btn-close-white" @click="showParticipants=false"></button>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4">#</th><th>Name</th><th>Email</th>
              <th>Contact</th><th>Booked On</th><th>Payment</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p,i) in participants" :key="p.booking_id">
              <td class="ps-4 small text-muted">{{ i+1 }}</td>
              <td class="small fw-semibold">{{ p.user_name }}</td>
              <td class="small text-muted">{{ p.email_id }}</td>
              <td class="small text-muted">{{ p.contact }}</td>
              <td class="small text-muted">{{ p.booking_date }}</td>
              <td>
                <span class="badge" :class="p.payment_status==='Paid'?'bg-success':'bg-warning text-dark'">
                  {{ p.payment_status }}
                </span>
              </td>
            </tr>
            <tr v-if="participants.length===0">
              <td colspan="6" class="text-center text-muted py-3">No participants yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Treks Table ── -->
    <div class="card border-0 shadow-sm">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">#</th>
              <th class="small text-secondary">Trek Name</th>
              <th class="small text-secondary">Location</th>
              <th class="small text-secondary">Difficulty</th>
              <th class="small text-secondary">Dates</th>
              <th class="small text-secondary">Slots</th>
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
            <tr v-for="t in filteredTreks" :key="t.trek_id">
              <td class="ps-4 text-muted small">{{ t.trek_id }}</td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <img :src="t.image" class="rounded" style="width:36px;height:36px;object-fit:cover"
                       @error="e=>e.target.src='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=60'" />
                  <span class="fw-semibold small">{{ t.trek_name }}</span>
                </div>
              </td>
              <td class="small text-muted"><i class="bi bi-geo-alt me-1"></i>{{ t.trek_Location }}</td>
              <td><span class="badge" :class="diffBadge(t.trek_difficulty)">{{ t.trek_difficulty }}</span></td>
              <td class="small text-muted">{{ t.start_date }}<br>{{ t.end_date }}</td>
              <td class="small">
                <span class="fw-semibold text-primary">{{ t.avilable_Slots }}</span>
                <span class="text-muted"> / {{ t.total_slots }}</span>
              </td>
              <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="openEditForm(t)" title="Edit">
                  <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-info me-1" @click="viewParticipants(t)" title="Participants">
                  <i class="bi bi-people"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteTrek(t.trek_id)" title="Delete">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>
            <tr v-if="!loading && filteredTreks.length===0">
              <td colspan="8" class="text-center text-muted py-4">No treks found</td>
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
  name: 'AdminTreks',

  // staffList is passed from parent AdminDash.vue
  props: {
    staffList: { type: Array, default: () => [] }
  },

  data() {
    return {
      treks:    [],
      loading:  false,
      search:   '',
      msg:      '', msgType: 'success',

      // Form state
      showForm: false,
      editId:   null,
      saving:   false,
      formMsg:  '', formMsgType: 'success',
      form: {
        trek_name: '', trek_Location: '', trek_difficulty: 'Easy',
        start_date: '', end_date: '', duration: 1,
        avilable_Slots: 10, price: 0, status: 'Open',
        assigned_staff_id: null, image: '', description: ''
      },

      // Participants panel
      showParticipants: false,
      currentTrek:      null,
      participants:     []
    }
  },

  computed: {
    filteredTreks() {
      if (!this.search.trim()) return this.treks
      const q = this.search.toLowerCase()
      return this.treks.filter(t =>
        t.trek_name.toLowerCase().includes(q) ||
        t.trek_Location.toLowerCase().includes(q)
      )
    }
  },

  mounted() {
    this.fetchTreks()
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

    async fetchTreks() {
      this.loading = true
      try {
        const r = await axios.get(`${API}/treks`)
        this.treks = r.data
      } catch (e) { console.error(e.message) }
      finally { this.loading = false }
    },

    openAddForm() {
      this.editId = null
      this.formMsg = ''
      this.form = {
        trek_name:'', trek_Location:'', trek_difficulty:'Easy',
        start_date:'', end_date:'', duration:1,
        avilable_Slots:10, price:0, status:'Open',
        assigned_staff_id:null, image:'', description:''
      }
      this.showForm = true
      this.showParticipants = false
    },

    openEditForm(t) {
      this.editId  = t.trek_id
      this.formMsg = ''
      this.form    = { ...t }
      this.showForm = true
      this.showParticipants = false
    },

    closeForm() {
      this.showForm = false
      this.editId   = null
      this.formMsg  = ''
    },

    async saveTrek() {
      if (!this.form.trek_name.trim())   { this.formMsg='Trek name is required';   this.formMsgType='danger'; return }
      if (!this.form.trek_Location.trim()){ this.formMsg='Location is required';   this.formMsgType='danger'; return }
      if (!this.form.start_date)          { this.formMsg='Start date is required'; this.formMsgType='danger'; return }
      if (!this.form.end_date)            { this.formMsg='End date is required';   this.formMsgType='danger'; return }

      this.saving = true; this.formMsg = ''
      try {
        if (this.editId) {
          await axios.put(`${API}/treks/${this.editId}`, this.form, { headers: this.authHeader() })
          this.msg = `Trek "${this.form.trek_name}" updated!`
        } else {
          await axios.post(`${API}/treks`, this.form, { headers: this.authHeader() })
          this.msg = `Trek "${this.form.trek_name}" added!`
        }
        this.msgType = 'success'
        this.closeForm()
        await this.fetchTreks()
        this.$emit('refresh-stats')
        setTimeout(() => this.msg = '', 4000)
      } catch (e) {
        this.formMsg     = e.response?.data?.message || 'Failed to save'
        this.formMsgType = 'danger'
      } finally { this.saving = false }
    },

    async deleteTrek(id) {
      if (!confirm('Delete this trek? All bookings will be removed.')) return
      try {
        await axios.delete(`${API}/treks/${id}`, { headers: this.authHeader() })
        this.msg     = 'Trek deleted'
        this.msgType = 'success'
        await this.fetchTreks()
        this.$emit('refresh-stats')
        setTimeout(() => this.msg = '', 3000)
      } catch (e) {
        this.msg = e.response?.data?.message || 'Delete failed'
        this.msgType = 'danger'
      }
    },

    async viewParticipants(trek) {
      this.currentTrek      = trek
      this.showParticipants = true
      this.showForm         = false
      this.participants     = []
      try {
        const r = await axios.get(`${API}/treks/${trek.trek_id}/participants`, { headers: this.authHeader() })
        this.participants = r.data
      } catch (e) { console.error(e.message) }
    }
  }
}
</script>
