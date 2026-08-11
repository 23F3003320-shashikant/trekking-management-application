<template>
  <div class="d-flex" style="min-height:100vh">
    <div class="sidebar d-flex flex-column" :class="{collapsed: sidebarCollapsed}">
      <div class="sidebar-brand d-flex align-items-center gap-2 p-3">
        <div class="brand-icon rounded-circle d-flex align-items-center justify-content-center flex-shrink-0">
          <i class="bi bi-mountains-fill text-white"></i>
        </div>
        <span class="brand-text fw-bold text-white small">Trekking Management<br><span class="text-white-50 fw-normal" style="font-size:0.7rem">Application</span></span>
      </div>

      <!-- Nav -->
      <nav class="flex-grow-1 px-2 py-2">
        <div v-for="item in navItems" :key="item.key">
          <button
            class="sidebar-nav-btn w-100 d-flex align-items-center gap-2 px-3 py-2 mb-1 rounded-2 border-0 text-start"
            :class="{ active: activeTab === item.key }"
            @click="$emit('navigate', item.key)">
            <i :class="`bi ${item.icon} flex-shrink-0`" style="font-size:1.05rem"></i>
            <span class="nav-text">{{ item.label }}</span>
            <span v-if="item.badge" class="badge bg-danger rounded-pill ms-auto nav-text" style="font-size:0.65rem">{{ item.badge }}</span>
          </button>
        </div>
      </nav>

      <!-- User info -->
      <div class="sidebar-footer p-3 border-top border-white-10">
        <div class="d-flex align-items-center gap-2">
          <div class="user-avatar rounded-circle d-flex align-items-center justify-content-center flex-shrink-0">
            <i class="bi bi-person-fill text-white" style="font-size:0.85rem"></i>
          </div>
          <div class="nav-text overflow-hidden">
            <div class="text-white fw-semibold text-truncate" style="font-size:0.82rem">{{ userName }}</div>
            <div class="text-white-50" style="font-size:0.7rem">{{ roleLabel }}</div>
          </div>
          <button class="btn btn-link p-0 ms-auto nav-text text-white-50" @click="logout" title="Logout">
            <i class="bi bi-box-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="main-content flex-grow-1 d-flex flex-column overflow-auto">
      <!-- Topbar -->
      <div class="topbar d-flex align-items-center justify-content-between px-4 py-3 bg-white border-bottom shadow-sm">
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-link p-0 text-muted" @click="sidebarCollapsed = !sidebarCollapsed">
            <i class="bi bi-list fs-5"></i>
          </button>
          <div>
            <h5 class="mb-0 fw-bold text-dark" style="font-size:1rem">{{ pageTitle }}</h5>
            <nav aria-label="breadcrumb">
              <ol class="breadcrumb mb-0" style="font-size:0.75rem">
                <li class="breadcrumb-item text-muted">{{ roleLabel }}</li>
                <li class="breadcrumb-item active text-primary">{{ pageTitle }}</li>
              </ol>
            </nav>
          </div>
        </div>
        <div class="d-flex align-items-center gap-3">
          <span class="badge rounded-pill" :class="roleBadgeClass" style="font-size:0.75rem">
            <i class="bi bi-person-fill me-1"></i>{{ roleLabel }}
          </span>
          <div class="text-end">
            <div class="fw-semibold text-dark" style="font-size:0.85rem">{{ userName }}</div>
            <div class="text-muted" style="font-size:0.72rem">{{ userEmail }}</div>
          </div>
          <button class="btn btn-outline-danger btn-sm" @click="logout">
            <i class="bi bi-box-arrow-right me-1"></i>Logout
          </button>
        </div>
      </div>

      <!-- Slot -->
      <div class="flex-grow-1 p-4 content-area">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidebarLayout',
  emits: ['navigate'],
  props: {
    activeTab: String,
    navItems: Array,
    pageTitle: { type: String, default: 'Dashboard' }
  },
  data() {
    return {
      sidebarCollapsed: false,
      userName: localStorage.getItem('name') || 'User',
      userEmail: localStorage.getItem('email_id') || '',
      role: localStorage.getItem('role') || 'trekker',
    }
  },
  computed: {
    roleLabel() {
      const m = { admin: 'Admin', staff: 'Trek Staff', trekker: 'Trekker' }
      return m[this.role] || this.role
    },
    roleBadgeClass() {
      const m = { admin: 'bg-primary', staff: 'bg-success', trekker: 'bg-warning text-dark' }
      return m[this.role] || 'bg-secondary'
    }
  },
  methods: {
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  min-width: 240px;
  background: linear-gradient(180deg, #1e3a5f 0%, #0d1b2a 100%);
  transition: width 0.25s ease, min-width 0.25s ease;
  overflow: hidden;
}
.sidebar.collapsed { width: 70px; min-width: 70px; }
.sidebar.collapsed .nav-text, .sidebar.collapsed .brand-text { display: none; }
.sidebar.collapsed .sidebar-nav-btn { justify-content: center; }
.brand-icon { width:36px;height:36px;background:linear-gradient(135deg,#6366f1,#3b82f6);flex-shrink:0; }
.sidebar-brand { border-bottom: 1px solid rgba(255,255,255,0.1); min-height: 64px; }
.sidebar-nav-btn { background: transparent; color: rgba(255,255,255,0.7); transition: all 0.15s; font-size: 0.85rem; }
.sidebar-nav-btn:hover { background: rgba(255,255,255,0.08); color: #fff; }
.sidebar-nav-btn.active { background: rgba(99,102,241,0.25); color: #fff; border-left: 3px solid #6366f1 !important; }
.user-avatar { width:32px;height:32px;background:rgba(255,255,255,0.2); }
.border-white-10 { border-color: rgba(255,255,255,0.1) !important; }
.topbar { min-height: 64px; }
.content-area { background: #f1f4f8; }
</style>
