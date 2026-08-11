<template>
  <SidebarLayout
    :activeTab="tab"
    :navItems="navItems"
    :pageTitle="pageTitle"
    @navigate="tab = $event">

    <AdminDashboard v-if="tab === 'dashboard'" :stats="stats" @go-tab="tab = $event" />
    <AdminTreks     v-if="tab === 'treks'"     :staffList="staffList" @refresh-stats="fetchStats" />
    <AdminStaff     v-if="tab === 'staff'"     @refresh-stats="fetchStats" @staff-updated="staffList = $event" />
    <AdminUsers     v-if="tab === 'users'"     @refresh-stats="fetchStats" />
    <AdminBookings  v-if="tab === 'bookings'"  @refresh-stats="fetchStats" />
    <AdminReports   v-if="tab === 'reports'"   :stats="stats" />

  </SidebarLayout>
</template>

<script>
import axios from 'axios'
import SidebarLayout   from './SidebarLayout.vue'
import AdminDashboard  from './admin/AdminDashboard.vue'
import AdminTreks      from './admin/AdminTreks.vue'
import AdminStaff      from './admin/AdminStaff.vue'
import AdminUsers      from './admin/AdminUsers.vue'
import AdminBookings   from './admin/AdminBooking.vue'
import AdminReports    from './admin/AdminReports.vue'

export default {
  name: 'AdminDash',

  components: {
    SidebarLayout,
    AdminDashboard,
    AdminTreks,
    AdminStaff,
    AdminUsers,
    AdminBookings,
    AdminReports
  },

  data() {
    return {
      tab: 'dashboard',

      navItems: [
        { key: 'dashboard', label: 'Dashboard',        icon: 'bi-speedometer2'      },
        { key: 'treks',     label: 'Treks',            icon: 'bi-signpost-2'        },
        { key: 'staff',     label: 'Trekking Staff',   icon: 'bi-person-badge'      },
        { key: 'users',     label: 'Users (Trekkers)', icon: 'bi-people'            },
        { key: 'bookings',  label: 'Bookings',         icon: 'bi-journal-bookmark'  },
        { key: 'reports',   label: 'Reports',          icon: 'bi-bar-chart'         },
      ],

      stats: {
        total_treks: 0, total_staff: 0,
        total_users: 0, total_bookings: 0,
        recent_bookings: []
      },

      staffList: []
    }
  },

  computed: {
    pageTitle() {
      const titles = {
        dashboard: 'Dashboard',
        treks:     'Treks',
        staff:     'Trekking Staff',
        users:     'Users (Trekkers)',
        bookings:  'Bookings',
        reports:   'Reports'
      }
      return titles[this.tab] || 'Dashboard'
    }
  },

  mounted() {
    this.fetchStats()
    this.fetchStaffList()
  },

  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async fetchStats() {
      try {
        const r = await axios.get('http://localhost:5000/stats', { headers: this.authHeader() })
        this.stats = r.data
      } catch (e) { console.error('fetchStats:', e.message) }
    },

    async fetchStaffList() {
      try {
        const r = await axios.get('http://localhost:5000/staff', { headers: this.authHeader() })
        this.staffList = r.data
      } catch (e) { console.error('fetchStaffList:', e.message) }
    }
  }
}
</script>
