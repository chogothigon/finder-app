<template>
  <section class="random-view">
    <div v-if="randomCar" class="random-card">
      <div class="random-layout">
        <div class="random-image-wrapper">
          <img
            v-if="randomCar.image_url && !imageFailed"
            :src="randomCar.image_url"
            alt="Random car image"
            class="car-image"
            @error="imageFailed = true"
          />
          <div v-else class="image-placeholder">No Image</div>
        </div>

        <div class="random-details">
          <h3 class="random-title">
            {{ randomCar.car_year }} {{ randomCar.car_make }} {{ randomCar.car_model }}
          </h3>

          <p><strong>VIN:</strong> {{ randomCar.car_vin }}</p>
          <p><strong>Arrival Date:</strong> {{ formattedArrivalDate }}</p>
          <p>
            <strong>Location:</strong>
            {{ randomCar.junkyard_city || 'Unknown' }},
            {{ randomCar.junkyard_state || 'Unknown' }}
            {{ randomCar.junkyard_zip || '' }}
          </p>
          <p><strong>Junkyard:</strong> {{ randomCar.junkyard_name || 'Unknown' }}</p>
          <p><strong>Engine Data:</strong> {{ randomCar.car_engine_data || 'Unknown' }}</p>

          <p>
            <strong>Source:</strong>
            <a
              v-if="randomCar.car_source"
              :href="randomCar.car_source"
              target="_blank"
              rel="noopener noreferrer"
              class="source-link"
            >
              {{ randomCar.junkyard_name || 'View Listing' }}
            </a>
            <span v-else>Unknown</span>
          </p>

        <button class="random-btn" @click="pickRandomCar">
          Show Another Random Car
        </button>

          <button
            class="fav-btn"
            @click.stop="handleFavorite"
            :title="favorited ? 'Remove from favorites' : 'Add to favorites'"
          >
            <span v-if="favorited">❤️</span>
            <span v-else>🤍</span>
          </button>
        </div>
      </div>
    </div>

    <p v-else>Loading random car...</p>

  </section>
</template>

<script>
export default {
  name: 'RandomView',
  data() {
    return {
      cars: [],
      randomCar: null,
      imageFailed: false
    }
  },
  computed: {
    formattedArrivalDate() {
      if (!this.randomCar?.car_arrival_date) return 'N/A'
      return new Date(this.randomCar.car_arrival_date).toLocaleDateString()
    }
  },
  async mounted() {
    try {
      const response = await fetch('/api/cars')
      const data = await response.json()
      this.cars = data
      this.pickRandomCar()
    } catch (error) {
      console.error('Failed to load random car:', error)
    }
  },
  methods: {
    pickRandomCar() {
      if (!this.cars.length) return

      const randomIndex = Math.floor(Math.random() * this.cars.length)
      this.randomCar = this.cars[randomIndex]
      this.imageFailed = false
    }
  }
}

</script>

<style scoped>
.random-view {
  padding: 30px;
}

.random-card {
  max-width: 900px;
  margin: 0 auto;
  border: 1px solid #d9d9d9;
  border-radius: 18px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 28px;
  box-sizing: border-box;
}

.random-layout {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
  align-items: flex-start;
}

.random-image-wrapper {
  width: 360px;
  max-width: 100%;
  height: 240px;
  background: #f2f2f2;
  overflow: hidden;
  border-radius: 14px;
}

.car-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 14px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
  font-size: 1.2rem;
  border-radius: 14px;
}

.random-details {
  flex: 1;
  min-width: 260px;
}

.random-title {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c3e50;
}

.random-details p {
  margin: 10px 0;
  color: #444;
  font-size: 1rem;
  word-break: break-word;
}

.random-btn {
  margin-top: 20px;
  padding: 12px 18px;
  border: none;
  border-radius: 10px;
  background-color: #2c3e50;
  color: white;
  cursor: pointer;
}

.source-link {
  color: #2c3e50;
  font-weight: 600;
  text-decoration: none;
}

.source-link:hover {
  text-decoration: underline;
}

.fav-btn {
  margin-left: 10px;
  padding: 12px 18px;
  border: none;
  border-radius: 10px;
  background-color: #f3f4f6;
  cursor: pointer;
  font-size: 1rem;
}
</style>