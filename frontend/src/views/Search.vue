<template>
  <section class="search-view">
    <SearchBar @search="doSearch" />
    <div class="car-grid" v-if="visibleResults.length">
      <CarCard v-for="car in visibleResults" :key="car.car_id" :car="car" @view-details="openCarModal" />
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

    <div
      v-if="selectedCar"
      class="modal-overlay"
      @click="closeCarModal"
    >
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="closeCarModal">×</button>

        <div class="modal-layout">
          <div class="modal-image-wrapper">
            <img
              v-if="selectedCar.image_url"
              :src="selectedCar.image_url"
              alt="Car image"
              class="modal-image"
            />
            <div v-else class="modal-image-placeholder">No Image</div>
          </div>

          <div class="modal-details">
            <h2 class="modal-title">
              {{ selectedCar.car_year }} {{ selectedCar.car_make }} {{ selectedCar.car_model }}
            </h2>

            <p><strong>VIN:</strong> {{ selectedCar.car_vin || 'Unknown' }}</p>
            <p><strong>Arrival Date:</strong> {{ formattedModalArrivalDate }}</p>
            <p>
              <strong>Location:</strong>
              {{ selectedCar.junkyard_city || 'Unknown' }},
              {{ selectedCar.junkyard_state || 'Unknown' }}
              {{ selectedCar.junkyard_zip || '' }}
            </p>
            <p><strong>Junkyard:</strong> {{ selectedCar.junkyard_name || 'Unknown' }}</p>
            <p><strong>Engine Data:</strong> {{ selectedCar.car_engine_data || 'Unknown' }}</p>
            <p><strong>Listing Active:</strong> {{ selectedCar.car_active ? 'Yes' : 'No' }}</p>

            <p>
              <strong>Source:</strong>
              <a
                v-if="selectedCar.car_source"
                :href="selectedCar.car_source"
                target="_blank"
                rel="noopener noreferrer"
                class="modal-source-link"
              >
                {{ selectedCar.junkyard_name || 'View Listing' }}
              </a>
              <span v-else>Unknown</span>
            </p>
          </div>
        </div>
      </div>
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
      currentlyVisible: 48,
      selectedCar: null
    }
  },
  computed: {
    visibleResults() {
      return this.searchResults.slice(0, this.currentlyVisible)
    },
    formattedModalArrivalDate() {
      if (!this.selectedCar?.car_arrival_date) return 'N/A'
      const date = new Date(this.selectedCar.car_arrival_date)
      return date.toLocaleDateString()
    },
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

      const matchesYear =
        !filters.year || String(car.car_year) === String(filters.year)

      const matchesZip =
      !filters.zip || String(car.junkyard_zip) === String(filters.zip)

      return matchesMake && matchesModel && matchesYear && matchesZip
    })

    this.currentlyVisible = 48

    console.log('Filters:', filters)
    console.log('Filtered results:', this.searchResults)
  },

  openCarModal(car) {
    this.selectedCar = car
  },

  closeCarModal() {
    this.selectedCar = null
  },

  loadMore() {
    this.currentlyVisible += 48
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
  grid-template-columns: repeat(4, 240px);
  justify-content: center;
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

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
  z-index: 2000;
}

.modal-content {
  background: white;
  width: min(900px, 95vw);
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 18px;
  padding: 28px;
  position: relative;
  box-sizing: border-box;
}

.close-button {
  position: absolute;
  top: 12px;
  right: 16px;
  border: none;
  background: transparent;
  font-size: 2rem;
  cursor: pointer;
  color: #2c3e50;
}

.modal-layout {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
  align-items: flex-start;
}

.modal-image-wrapper {
  width: 360px;
  max-width: 100%;
}

.modal-image {
  width: 100%;
  border-radius: 14px;
  object-fit: cover;
  display: block;
}

.modal-image-placeholder {
  width: 100%;
  height: 240px;
  background: #f2f2f2;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
}

.modal-details {
  flex: 1;
  min-width: 260px;
}

.modal-title {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c3e50;
}

.modal-details p {
  margin: 10px 0;
  color: #444;
  font-size: 1rem;
  word-break: break-word;
}

.modal-source-link {
  color: #2c3e50;
  font-weight: 600;
  text-decoration: none;
}

.modal-source-link:hover {
  text-decoration: underline;
}
</style>