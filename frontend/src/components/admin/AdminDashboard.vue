
<template>
  <div>
    <!-- Stat Cards Row -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-primary bg-opacity-10">
              <i class="bi bi-signpost-2 fs-4 text-primary"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold text-dark">{{ stats.total_treks }}</div>
              <div class="text-muted small">Total Treks</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-info bg-opacity-10">
              <i class="bi bi-people fs-4 text-info"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold text-dark">{{ stats.total_users }}</div>
              <div class="text-muted small">Total Trekkers</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-success bg-opacity-10">
              <i class="bi bi-person-badge fs-4 text-success"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold text-dark">{{ stats.total_staff }}</div>
              <div class="text-muted small">Total Trekking Staff</div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="p-3 rounded-3 bg-warning bg-opacity-10">
              <i class="bi bi-journal-bookmark fs-4 text-warning"></i>
            </div>
            <div>
              <div class="fs-2 fw-bold text-dark">{{ stats.total_bookings }}</div>
              <div class="text-muted small">Total Bookings</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Bookings Table -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center py-3">
        <h6 class="mb-0 fw-bold">Recent Bookings</h6>
        <button class="btn btn-link btn-sm p-0 text-decoration-none" @click="$emit('go-tab', 'bookings')">
          View All Bookings →
        </button>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4">Booking ID</th>
              <th>Trekker</th>
              <th>Trek</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in stats.recent_bookings" :key="b.booking_id">
              <td class="ps-4 fw-semibold text-primary">#{{ b.booking_id }}</td>
              <td class="small">{{ b.user_name }}</td>
              <td class="small fw-semibold">{{ b.trek_name }}</td>
              <td class="text-muted small">{{ b.booking_date }}</td>
              <td>
                <span class="badge rounded-pill"
                  :class="b.status === 'Confirmed' ? 'bg-success' : 'bg-danger'">
                  {{ b.status }}
                </span>
              </td>
            </tr>
            <tr v-if="!stats.recent_bookings || stats.recent_bookings.length === 0">
              <td colspan="5" class="text-center text-muted py-3">No bookings yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Charts Row (vue-chartjs) -->
    <div class="row g-4">
      <!-- Bar Chart: Bookings per Trek -->
      <div class="col-md-8">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom py-3">
            <h6 class="mb-0 fw-bold">Bookings Per Trek</h6>
          </div>
          <div class="card-body">
            <div v-if="bookingChartLoading" class="text-center py-4">
              <div class="spinner-border spinner-border-sm text-primary"></div>
            </div>
            <Bar v-else-if="bookingChartData" :data="bookingChartData" :options="barOptions" style="max-height:260px"/>
          </div>
        </div>
      </div>

      <!-- Doughnut Chart: Difficulty Split -->
      <div class="col-md-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom py-3">
            <h6 class="mb-0 fw-bold">Treks by Difficulty</h6>
          </div>
          <div class="card-body d-flex align-items-center justify-content-center">
            <div v-if="diffChartLoading" class="text-center py-4">
              <div class="spinner-border spinner-border-sm text-primary"></div>
            </div>
            <Doughnut v-else-if="diffChartData" :data="diffChartData" :options="doughnutOptions" style="max-height:240px"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
// Import chart components from vue-chartjs
import { Bar, Doughnut } from 'vue-chartjs'
// Import and register Chart.js components we need
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale,
  ArcElement
} from 'chart.js'

// Register all needed chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

export default {
  name: 'AdminDashboard',

  // Register the chart components so we can use <Bar> and <Doughnut> in template
  components: { Bar, Doughnut },

  // Props passed in from AdminDash.vue
  props: {
    stats: {
      type: Object,
      default: () => ({
        total_treks: 0, total_staff: 0,
        total_users: 0, total_bookings: 0,
        recent_bookings: []
      })
    }
  },

  emits: ['go-tab'],

  data() {
    return {
      // Chart data objects (null until loaded)
      bookingChartData:  null,
      diffChartData:     null,
      bookingChartLoading: true,
      diffChartLoading:    true,

      // Chart display options
      barOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          title:  { display: false }
        },
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 1 } }
        }
      },

      doughnutOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { position: 'bottom' }
        }
      }
    }
  },

  mounted() {
    // Load chart data when component is created
    this.loadBookingChart()
    this.loadDiffChart()
  },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    // Load bar chart: bookings per trek
    async loadBookingChart() {
      this.bookingChartLoading = true
      try {
        const r = await axios.get('http://localhost:5000/charts/bookings-per-trek', {
          headers: this.authHeader()
        })
        // vue-chartjs needs data in this exact format
        this.bookingChartData = {
          labels: r.data.labels,
          datasets: [{
            label: 'Bookings',
            data: r.data.values,
            backgroundColor: [
              '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#8b5cf6'
            ],
            borderRadius: 6,
            borderSkipped: false
          }]
        }
      } catch (e) {
        console.error('Chart load failed:', e.message)
      } finally {
        this.bookingChartLoading = false
      }
    },

    // Load doughnut chart: difficulty split
    async loadDiffChart() {
      this.diffChartLoading = true
      try {
        const r = await axios.get('http://localhost:5000/charts/difficulty-split', {
          headers: this.authHeader()
        })
        this.diffChartData = {
          labels: r.data.labels,
          datasets: [{
            data: r.data.values,
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#1f2937'],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        }
      } catch (e) {
        console.error('Chart load failed:', e.message)
      } finally {
        this.diffChartLoading = false
      }
    }
  }
}
</script>
