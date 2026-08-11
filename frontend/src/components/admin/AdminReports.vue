
<template>
    <!-- Stat cards (same as dashboard) -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-primary bg-opacity-10">
              <i class="bi bi-signpost-2 fs-4 text-primary"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ stats.total_treks }}</div>
              <div class="text-muted small">Total Treks</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-info bg-opacity-10">
              <i class="bi bi-people fs-4 text-info"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ stats.total_users }}</div>
              <div class="text-muted small">Total Trekkers</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-success bg-opacity-10">
              <i class="bi bi-person-badge fs-4 text-success"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ stats.total_staff }}</div>
              <div class="text-muted small">Total Staff</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-warning bg-opacity-10">
              <i class="bi bi-journal-bookmark fs-4 text-warning"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold">{{ stats.total_bookings }}</div>
              <div class="text-muted small">Total Bookings</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Slots Bar Chart  -->
    <div class="row g-4 mb-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-bottom py-3">
            <h6 class="mb-0 fw-bold">Available vs Filled Slots per Trek</h6>
          </div>
          <div class="card-body">
            <div v-if="chartLoading" class="text-center py-4">
              <div class="spinner-border spinner-border-sm text-primary"></div>
            </div>
            <Bar v-else-if="slotsChartData"
              :data="slotsChartData"
              :options="barOptions"
              style="max-height:260px" />
          </div>
      </div>

    <!-- Report Table -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h6 class="mb-0 fw-bold">Trek-wise Booking Report</h6>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4 small text-secondary">Trek Name</th>
              <th class="small text-secondary">Location</th>
              <th class="small text-secondary">Difficulty</th>
              <th class="small text-secondary">Total Slots</th>
              <th class="small text-secondary">Filled</th>
              <th class="small text-secondary">Available</th>
              <th class="small text-secondary">Fill Rate</th>
              <th class="small text-secondary">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="tableLoading">
              <td colspan="8" class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary me-2"></div>Loading...
              </td>
            </tr>
            <tr v-for="r in reportData" :key="r.trek_name">
              <td class="ps-4 fw-semibold small">{{ r.trek_name }}</td>
              <td class="small text-muted"><i class="bi bi-geo-alt me-1"></i>{{ r.trek_location }}</td>
              <td>
                <span class="badge" :class="diffBadge(r.trek_difficulty)">{{ r.trek_difficulty }}</span>
              </td>
              <td class="text-center small fw-semibold">{{ r.total_slots }}</td>
              <td class="text-center small fw-semibold text-success">{{ r.slots_filled }}</td>
              <td class="text-center small fw-semibold text-primary">{{ r.available_slots }}</td>
              <td style="min-width:150px">
                <div class="d-flex align-items-center gap-2">
                  <div class="progress flex-grow-1" style="height:7px">
                    <div class="progress-bar"
                      :class="r.fill_rate > 75 ? 'bg-success' : r.fill_rate > 40 ? 'bg-warning' : 'bg-primary'"
                      :style="`width:${r.fill_rate}%`">
                    </div>
                  </div>
                  <small class="text-muted fw-semibold" style="min-width:38px">{{ r.fill_rate }}%</small>
                </div>
              </td>
              <td>
                <span class="badge" :class="statusBadge(r.status)">{{ r.status }}</span>
              </td>
            </tr>
            <tr v-if="!tableLoading && reportData.length === 0">
              <td colspan="8" class="text-center text-muted py-4">No report data</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const API = 'http://localhost:5000'

export default {
  name: 'AdminReports',
  components: { Bar },

  props: {
    stats: {
      type: Object,
      default: () => ({
        total_treks: 0, total_staff: 0,
        total_users: 0, total_bookings: 0
      })
    }
  },

  data() {
    return {
      reportData:     [],
      tableLoading:   false,
      chartLoading:   false,
      slotsChartData: null,
      emailMsg:       '',
      emailSuccess:   true,
      emailSending:   false,

      barOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { position: 'bottom' }
        },
        scales: {
          x: { stacked: false },
          y: { beginAtZero: true, ticks: { stepSize: 1 } }
        }
      }
    }
  },

  mounted() {
    this.fetchReport()
    this.loadSlotsChart()
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

    async fetchReport() {
      this.tableLoading = true
      try {
        const r = await axios.get(`${API}/reports`, { headers: this.authHeader() })
        this.reportData = r.data
      } catch (e) { console.error(e.message) }
      finally { this.tableLoading = false }
    },

    async loadSlotsChart() {
      this.chartLoading = true
      try {
        const r = await axios.get(`${API}/charts/slots-status`, { headers: this.authHeader() })
        // Grouped bar chart: available vs filled slots
        this.slotsChartData = {
          labels: r.data.labels,
          datasets: [
            {
              label: 'Available Slots',
              data: r.data.available,
              backgroundColor: '#3b82f6',
              borderRadius: 4
            },
            {
              label: 'Filled Slots',
              data: r.data.filled,
              backgroundColor: '#10b981',
              borderRadius: 4
            }
          ]
        }
      } catch (e) { console.error(e.message) }
      finally { this.chartLoading = false }
    },

  }
}
</script>
