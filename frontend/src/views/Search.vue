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
  },
  data() {
    return {
      cars: []
    }
  },
  async mounted() {
    try {
      const response = await fetch('/api/cars')
      const data = await response.json()
      this.cars = data
    } catch (error) {
      console.error('CANNOT FETCH CARS:', error)
    }
  }
}
</script>