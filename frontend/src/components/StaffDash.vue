
<template>
  <SidebarLayout
    :activeTab="tab"
    :navItems="navItems"
    :pageTitle="pageTitle"
    @navigate="switchTab">

    <StaffDashboard
      v-if="tab === 'dashboard'"
      @manage-trek="selectTrek" />

    <StaffMyTreks
      v-if="tab === 'mytreks'"
      :trek="selectedTrek"
      @go-tab="tab = $event" />

    <StaffProfile
      v-if="tab === 'profile'" />

  </SidebarLayout>
</template>

<script>
import SidebarLayout   from './SidebarLayout.vue'
import StaffDashboard  from './staff/StaffDashboard.vue'
import StaffMyTreks    from './staff/StaffMyTreks.vue'
import StaffProfile    from './staff/StaffProfile.vue'

export default {
  name: 'StaffDash',

  components: {
    SidebarLayout,
    StaffDashboard,
    StaffMyTreks,
    StaffProfile
  },

  data() {
    return {
      tab: 'dashboard',
      selectedTrek: null,     // trek passed to StaffMyTreks

      navItems: [
        { key: 'dashboard', label: 'My Dashboard', icon: 'bi-speedometer2'   },
        { key: 'mytreks',   label: 'My Treks',     icon: 'bi-signpost-2'     },
        { key: 'profile',   label: 'Profile',      icon: 'bi-person-circle'  },
      ]
    }
  },

  computed: {
    pageTitle() {
      const titles = {
        dashboard: 'My Dashboard',
        mytreks:   'Manage Trek',
        profile:   'My Profile'
      }
      return titles[this.tab] || 'Dashboard'
    }
  },

  methods: {
    switchTab(t) {
      this.tab = t
    },

    selectTrek(trek) {
      this.selectedTrek = { ...trek }
      this.tab = 'mytreks'
    }
  }
}
</script>
