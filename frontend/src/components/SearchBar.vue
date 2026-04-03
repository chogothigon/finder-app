<template>
  <div class="search-bar">
    <div class="field-group">
      <label for="make">Make</label>
      <select id="make" v-model="selectedMake">
        <option disabled value="">Select</option>
        <option 
        v-for="make in uniqueMakes" :key="make" :value="make">{{ make }}
        </option>
      </select>
    </div>

    <div class="field-group">
      <label for="model">Model</label>
      <select id="model" v-model="selectedModel" :disabled="!selectedMake">
        <option disabled value="">Select</option>
        <option 
        v-for="model in uniqueModels" :key="model" :value="model">{{ model }}
        </option>
      </select>
    </div>


    <div class="field-group">
      <label for="zip">ZIP</label>
      <input type="text" id="zip">
    </div>

    <button @click="doSearch">Search</button>

  </div>

  
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      cars: [],
      uniqueMakes: [],
      uniqueModels: [],
      selectedMake: '',
      selectedModel: ''
    }
  },
  
   async mounted() {
    try {
      console.log('SearchBar mounted')

      const response = await fetch('/api/cars')
      console.log('response ok:', response.ok)

      const data = await response.json()
      console.log('data:', data)

      this.cars = data

      const makes = data.map(car => car.car_make).filter(Boolean)
      console.log('makes:', makes)

      this.uniqueMakes = [...new Set(makes)].sort()
      console.log('uniqueMakes:', this.uniqueMakes)
    } catch (err) {
      console.error('Error loading makes:', err)
    }
  },
  watch: {
  selectedMake(newMake) {
    if (!newMake) {
      this.uniqueModels = []
      this.selectedModel = ''
      return
    }

    const models = this.cars
      .filter(car => car.car_make === newMake)
      .map(car => car.car_model)
      .filter(Boolean)

    this.uniqueModels = [...new Set(models)].sort()
    this.selectedModel = ''
  }
},
methods: {
  doSearch() {
    this.$emit('search', {
      make: this.selectedMake,
      model: this.selectedModel
    })
  }
}
}
</script>

<style scoped>
.search-bar {
  width: 95%;
  margin: 20px auto;
  padding: 24px;
  border: 1px solid #d9d9d9;
  border-radius: 16px;
  background-color: white;
  box-sizing: border-box;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 30px;
}

.field-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

label {
  font-size: 1.2rem;
  font-weight: 500;
  color: #2c3e50;
}

select{
  font-size: 1.1rem;
  padding: 10px 14px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  background-color: white;
  color: #2c3e50;
  width: 200px;
}
input {
  font-size: 1.1rem;
  padding: 10px 14px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  background-color: white;
  color: #2c3e50;
  width: 220px;
}
</style>