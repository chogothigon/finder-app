<template>
  <nav class="navbar">
    <h1>Parts Finder</h1>
    <div class="nav-inner">
      <router-link to="/" class="nav-item">Search</router-link>
      <router-link to="/about" class="nav-item">About</router-link>
      <router-link to="/random" class="nav-item">Random</router-link>
      <router-link to="/donate" class="nav-item">Donate</router-link>
      <router-link to="/login" class="nav-item">Login</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.navbar {
  width: 95%;
  margin: 20px auto;
  border: 1px solid #d9d9d9;
  border-radius: 16px;
  background-color: white;
  padding: 18px 24px;
  box-sizing: border-box;
}

.nav-inner {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
  flex-wrap: wrap;
}

.nav-item {
  text-decoration: none;
  color: #2c3e50;
  font-size: 1.2rem;
  font-weight: 500;
}

.nav-item:hover {
  color: #42b983;
}
</style>