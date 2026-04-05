<template>
  <div class="car-card">
    <div class="image-wrapper">
      <img
        v-if="car.image_url"
        :src="car.image_url"
        alt="Car image"
        class="car-image"
      />
      <div v-else class="image-placeholder">
        <span>No Image</span>
      </div>
    </div>

    <div class="card-content">
      <div class="card-header">
        <h3 class="car-title">{{ car.car_make }} {{ car.car_model }}</h3>
        <button
          class="fav-btn"
          @click.stop="handleFavorite"
          :title="favorited ? 'Remove from favorites' : 'Add to favorites'"
        >
          <span v-if="favorited">❤️</span>
          <span v-else>🤍</span>
        </button>
      </div>
 
      <p class="car-year">Year: {{ car.car_year }}</p>
      <p class="car-vin">VIN: {{ car.car_vin }}</p>
      <p class="car-date">Arrival Date: {{ formattedArrivalDate }}</p>
 
      <a
        class="source-link"
        :href="car.car_source"
        target="_blank"
        rel="noopener noreferrer"
      >
        View Source
      </a>
    </div>
  </div>
</template>

<script>
import { initFavorites, isFavorited, toggleFavorite, favoritesState } from '@/composables/useFavorites'

export default {
  name: 'CarCard',
  props: {
    car: {
      type: Object,
      required: true
    }
  },
  computed: {
    favorited() {
      return isFavorited(this.car.car_id)
    },

    _favState() {
      return favoritesState.favorites
    },

    formattedArrivalDate() {
      if (!this.car.car_arrival_date) return 'N/A'
      const date = new Date(this.car.car_arrival_date)
      return date.toLocaleDateString()
    }
  },
  async mounted() {
    // initFavorites is safe to call multiple times — it's a no-op after first run
    await initFavorites()
  },
  methods: {
    async handleFavorite() {
      await toggleFavorite(this.car.car_id)
    }
  }
}
</script>

<style scoped>
.car-card {
  width: 240px;
  border: 1px solid #d9d9d9;
  border-radius: 16px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
}

.image-wrapper {
  width: 100%;
  height: 160px;
  background-color: #f2f2f2;
  overflow: hidden;
}

.car-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  height: 160px;
  background-color: #f2f2f2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
  font-size: 1rem;
  font-weight: 500;
}

.card-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

fav-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0 0 0 8px;
  line-height: 1;
  flex-shrink: 0;
}

.car-title {
  margin: 0 0 12px 0;
  font-size: 1.2rem;
  color: #2c3e50;
}

.car-year,
.car-vin,
.car-date {
  margin: 6px 0;
  color: #444;
  font-size: 0.95rem;
  word-break: break-word;
}

.source-link {
  display: inline-block;
  margin-top: 12px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: 600;
}

.source-link:hover {
  text-decoration: underline;
}
</style>