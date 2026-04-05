<template>
  <section class="random-view">
    <div v-if="randomCar" class="random-card">
      <div class="image-wrapper">
        <img
          v-if="randomCar.image_url && !imageFailed"
          :src="randomCar.image_url"
          alt="Random car image"
          class="car-image"
          @error="imageFailed = true"
        />
        <div v-else class="image-placeholder">No Image</div>
      </div>

      <div class="card-content">
        <h3>{{ randomCar.car_make }} {{ randomCar.car_model }}</h3>
        <p><strong>Year:</strong> {{ randomCar.car_year }}</p>
        <p><strong>VIN:</strong> {{ randomCar.car_vin }}</p>
        <p><strong>Arrival Date:</strong> {{ formattedArrivalDate }}</p>
        <p><strong>Source:</strong></p>

        <a
          :href="randomCar.car_source"
          target="_blank"
          rel="noopener noreferrer"
        >
          View Source
        </a>

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
  max-width: 700px;
  margin: 0 auto;
  border: 1px solid #d9d9d9;
  border-radius: 18px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.image-wrapper {
  width: 100%;
  height: 320px;
  background: #f2f2f2;
  overflow: hidden;
}

.car-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
  font-size: 1.2rem;
}

.card-content {
  padding: 24px;
}

.card-content h3 {
  margin-top: 0;
  font-size: 2rem;
  color: #2c3e50;
}

.card-content p {
  margin: 10px 0;
  font-size: 1.05rem;
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
</style>