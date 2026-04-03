<template>
  <section class="search-view">
    <h2>Search</h2>
    <SearchBar @search="doSearch" />
    <div class="car-grid" v-if="visibleResults.length">
      <CarCard v-for="car in visibleResults" :key="car.car_id" :car="car" />
    </div>

    <p v-else class="no-results">Sorry, no cars yet {{':('}}</p>

    <div
      class="load-more-wrapper"
      v-if="searchResults.length > currentlyVisible"
    >
      <button class="load-more-btn" @click="loadMore">
        Load More
      </button>
    </div>

  </section>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import CarCard from '../components/CarCard.vue'

export default {
  name: 'SearchView',
  components: {
    SearchBar,
    CarCard
  },
  data() {
    return {
      cars: [],
      searchResults: [],
      currentlyVisible: 50
    }
  },
  computed: {
    visibleResults() {
      return this.searchResults.slice(0, this.currentlyVisible)
    }
  },
  async mounted() {
    try {
      const response = await fetch('/api/cars')
      const data = await response.json()
      this.cars = data
      this.searchResults = data
    } catch (error) {
      console.error('CANNOT FETCH CARS:', error)
    }
  },
  methods: {
  doSearch(filters) {
    this.searchResults = this.cars.filter(car => {
      const matchesMake =
        !filters.make || car.car_make === filters.make

      const matchesModel =
        !filters.model || car.car_model === filters.model

      return matchesMake && matchesModel
    })

    this.currentlyVisible = 50

    console.log('Filters:', filters)
    console.log('Filtered results:', this.searchResults)
  },
  loadMore() {
    this.currentlyVisible += 50
  }
}
}
</script>

<style scoped>
.search-view {
  padding: 20px;
}

.car-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 30px;
}

.load-more-wrapper {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}

.load-more-btn {
  font-size: 1rem;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  background-color: #2c3e50;
  color: white;
  cursor: pointer;
}

.load-more-btn:hover {
  opacity: 0.9;
}

.no-results {
  text-align: center;
  margin-top: 30px;
  color: #666;
  font-size: 1.1rem;
}
</style>