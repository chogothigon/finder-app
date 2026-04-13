import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

<v-btn
  href="/api/v1/auth/google"
  color="primary"
  size="large"
  prepend-icon="mdi-google"
  class="mt-4"
>
  Sign in with Google
</v-btn>

createApp(App).use(router).mount('#app')