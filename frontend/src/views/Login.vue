<template>
  <div id='login'>
    <h1>Welcome to your Task List!</h1>
    <v-btn :href="`${apiOrigin}/api/v1/auth/google`" color="primary">
      <v-icon left>mdi-google</v-icon>
      Log In with Google
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data: () => ({
    apiOrigin: process.env.VUE_APP_API_ORIGIN
  })
}
</script>

<style scoped>
#login {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  height: 50%;
}
</style>