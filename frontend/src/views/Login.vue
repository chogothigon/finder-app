<template>
  <div id='login'>
    <div v-if="user" class="logged-in">
      <v-avatar size="72" class="mb-4">
        <v-img v-if="user.avatar" :src="user.avatar" :alt="user.name" />
        <v-icon v-else size="48">mdi-account-circle</v-icon>
      </v-avatar>
      <h2>Welcome, {{ user.name }}!</h2>
      <p class="email">{{ user.email }}</p>
      <v-btn
        class="mt-4"
        color="error"
        variant="outlined"
        @click="logout"
      >
        Sign Out
      </v-btn>
    </div>
 
    <div v-else class="logged-out">
      <h1>Sign In</h1>
      <p class="subtitle">Sign in to save your favorite cars.</p>
      <v-btn
        :href="`${apiOrigin}/api/v1/auth/google`"
        color="primary"
        size="large"
        prepend-icon="mdi-google"
        class="mt-4"
      >
        Sign in with Google
      </v-btn>
    </div>
  </div>
</template>
      

<script>
export default {
  name: 'LoginView',
  data: () => ({
    apiOrigin: process.env.VUE_APP_API_ORIGIN,
    user: null
  }),
  async mounted() {
    try {
      const res = await fetch('/api/v1/auth/me', { credentials: 'include' })
      if (res.ok) this.user = await res.json()
    } catch (e) {
      // not logged in
    }
  },
  methods: {
    async logout() {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        credentials: 'include'
      })
      this.user = null
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
#login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.logged-in,
.logged-out {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 8px;
}

h2 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin-bottom: 4px;
}

.subtitle {
  color: #665;
  font-size: 1rem;
  margin-bottom: 8px;
}

.email {
  color: #888;
  font-size: 0.9rem;
}

</style>