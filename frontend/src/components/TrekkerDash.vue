<template>
  <SidebarLayout
    :activeTab="tab"
    :navItems="navItems"
    :pageTitle="pageTitle"
    @navigate="tab = $event">

    <TrekkerDashboard
      v-if="tab === 'dashboard'"
      @go-tab="tab = $event"
      @bookings-changed="bookedIds = $event" />

    <TrekkerBrowse
      v-if="tab === 'browse'"
      :bookedIds="bookedIds"
      @booking-changed="refreshBookedIds" />

    <TrekkerBookings
      v-if="tab === 'mybookings'"
      @bookings-loaded="bookedIds = $event"
      @go-browse="tab = 'browse'" />

    <TrekkerHistory
      v-if="tab === 'history'" />

    <TrekkerProfile
      v-if="tab === 'profile'" />

  </SidebarLayout>
</template>

<script>
import axios from 'axios'
import SidebarLayout      from './SidebarLayout.vue'
import TrekkerDashboard   from './trekker/TrekkerDashboard.vue'
import TrekkerBrowse      from './trekker/TrekkerBrowse.vue'
import TrekkerBookings    from './trekker/TrekkerBookings.vue'
import TrekkerHistory     from './trekker/TrekkerHistory.vue'
import TrekkerProfile     from './trekker/TrekkerProfile.vue'

const API = 'http://localhost:5000'

export default {
  name: 'TrekkerDash',

  components: {
    SidebarLayout,
    TrekkerDashboard,
    TrekkerBrowse,
    TrekkerBookings,
    TrekkerHistory,
    TrekkerProfile
  },

  data() {
    return {
      tab: 'dashboard',

      // Shared Set of trek_ids already booked — keeps Browse in sync
      bookedIds: new Set(),

      navItems: [
        { key: 'dashboard',  label: 'Dashboard',    icon: 'bi-speedometer2'     },
        { key: 'browse',     label: 'Browse Treks', icon: 'bi-binoculars'       },
        { key: 'mybookings', label: 'My Bookings',  icon: 'bi-journal-bookmark' },
        { key: 'history',    label: 'History',      icon: 'bi-clock-history'    },
        { key: 'profile',    label: 'Profile',      icon: 'bi-person-circle'    },
      ]
    }
  },

  computed: {
    pageTitle() {
      const titles = {
        dashboard:  'Dashboard',
        browse:     'Browse Treks',
        mybookings: 'My Bookings',
        history:    'Trekking History',
        profile:    'My Profile'
      }
      return titles[this.tab] || 'Dashboard'
    }
  },

  methods: {
    // Called when TrekkerBrowse makes a new booking —
    // fetches latest booking ids so bookedIds stays in sync across tabs
    async refreshBookedIds() {
      try {
        const r = await axios.get(`${API}/bookings`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        this.bookedIds = new Set(r.data.map(b => Number(b.trek_id)))
      } catch (e) { console.error(e.message) }
    }
  }
}
</script>
