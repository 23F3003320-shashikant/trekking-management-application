<template>
  <div style="font-family:'Inter',sans-serif">

    <!-- show register or login panel inline -->
    <div v-if="showLogin">
      <LoginPage />
    </div>
    <div v-else-if="showRegister">
      <RegistrationPage />
    </div>

    <!-- LANDING PAGE -->
    <div v-else>
      <!-- NAVBAR -->
      <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background:rgba(13,27,42,0.95);backdrop-filter:blur(10px)">
        <div class="container">
          <span class="navbar-brand d-flex align-items-center gap-2 fw-bold">
            <div class="rounded-circle d-flex align-items-center justify-content-center"
                 style="width:34px;height:34px;background:linear-gradient(135deg,#6366f1,#3b82f6)">
              <i class="bi bi-mountains-fill text-white" style="font-size:0.85rem"></i>
            </div>
            Trekking <span class="text-primary ms-1">Management</span>
          </span>
          <div class="ms-auto d-flex gap-2">
            <button class="btn btn-outline-light btn-sm px-3" @click="showLogin = true">Login</button>
            <button class="btn btn-primary btn-sm px-3"       @click="showRegister = true">Register Free</button>
          </div>
        </div>
      </nav>

      <!-- MAIN -->
      <section class="hero-section d-flex align-items-center" style="min-height:100vh;position:relative;overflow:hidden">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <div class="container position-relative" style="z-index:2">
          <div class="row align-items-center">
            <div class="col-lg-6">
              <h1 class="text-white fw-black mb-4 lh-1" style="font-size:clamp(2.4rem,5.5vw,4rem)">
                Your Next<br>
                <span style="background:linear-gradient(90deg,#818cf8,#60a5fa,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent">
                  World
                </span><br>Adventure Awaits
              </h1>
              <p class="mb-4 lh-relaxed" style="color:rgba(255,255,255,0.75);font-size:1.1rem;max-width:480px">
                Discover breathtaking trails across the World. Book curated treks, track your journey and connect with expert guides.
              </p>
              <div class="d-flex gap-3 flex-wrap">
                <button class="btn btn-primary btn-lg px-5 fw-semibold" @click="showRegister = true">
                  <i class="bi bi-person-plus me-2"></i>Start Trekking
                </button>
                <button class="btn btn-outline-light btn-lg px-4" @click="showLogin = true">Login</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FEATURES BAR -->
      <div class="py-3" style="background:#1e3a5f">
        <div class="container">
          <div class="row g-2 text-white text-center">
            <div class="col-6 col-md-3" v-for="f in features" :key="f.label">
              <div class="d-flex align-items-center justify-content-center gap-2">
                <i :class="`bi ${f.icon} text-primary`"></i>
                <span class="small fw-semibold">{{ f.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import LoginPage       from '../components/LoginPage.vue'
import RegistrationPage from '../components/RegistrationPage.vue'

export default {
  name: 'HomePage',
  components: { LoginPage, RegistrationPage },
  data() {
    return {
      showLogin: false, showRegister: false,
      treks: [], loading: false, activeFilter: 'All',
  
      features: [
        { icon:'bi-shield-check',  label:'Verified Guides' },
        { icon:'bi-geo-alt',       label:'GPS Tracking'    },
        { icon:'bi-headset',       label:'24/7 Support'    },
        { icon:'bi-credit-card',   label:'Secure Booking'  },
      ],
    }
  },
  computed: {
    featuredTreks() { return this.treks.filter(t => t.status === 'Open').slice(0, 3) },
    displayedTreks() {
      const list = this.activeFilter === 'All' ? this.treks : this.treks.filter(t => t.trek_difficulty === this.activeFilter)
      return list.slice(0, 6)
    }
  },
  mounted() { this.fetchTreks() },
  methods: {
    diffBadge(d) {
      return { Easy:'bg-success', Moderate:'bg-warning text-dark', Hard:'bg-danger', Expert:'bg-dark' }[d] || 'bg-secondary'
    },
    async fetchTreks() {
      this.loading = true
      try { const r = await axios.get('http://localhost:5000/treks'); this.treks = r.data }
      catch (e) { /* backend may not be running */ }
      finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.hero-section { padding-top:72px; }
.hero-bg { position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1400&q=80') center/cover no-repeat; }
.hero-overlay { position:absolute;inset:0;background:linear-gradient(135deg,rgba(13,27,42,0.92),rgba(15,52,96,0.85),rgba(0,0,0,0.7)); }
.trek-card { transition:transform .2s,box-shadow .2s; }
.trek-card:hover { transform:translateY(-4px);box-shadow:0 10px 28px rgba(0,0,0,0.15) !important; }
.text-white-75 { color:rgba(255,255,255,0.75) !important; }
</style>


