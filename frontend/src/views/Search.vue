<template>
  <section>
    <h2>Search</h2>
    <SearchBar />
  </section>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'

export default {
  name: 'SearchView',
  components: {
    SearchBar
  }
}
</script>