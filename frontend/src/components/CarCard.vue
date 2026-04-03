<template>
  <div class="car-card">
    <div class="image-placeholder">
      <span>No Image</span>
    </div>

    <div class="card-content">
      <h3 class="car-title">{{ car.car_make }} {{ car.car_model }}</h3>

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
export default {
  name: 'CarCard',
  props: {
    car: {
      type: Object,
      required: true
    }
  },
  computed: {
    formattedArrivalDate() {
      if (!this.car.car_arrival_date) return 'N/A'

      const date = new Date(this.car.car_arrival_date)
      return date.toLocaleDateString()
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