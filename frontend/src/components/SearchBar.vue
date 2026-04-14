<template>
  <div class="search-bar">
    <div class="field-group">
      <label for="make">Make</label>
      <select id="make" v-model="selectedMake">
        <option value="">Select</option>
        <option 
        v-for="make in uniqueMakes" :key="make" :value="make">{{ make }}
        </option>
      </select>
    </div>

  

    <div class="field-group">
      <label for="model">Model</label>
      <select id="model" v-model="selectedModel">
        <option value="">Select</option>
        <option 
        v-for="model in uniqueModels" :key="model" :value="model">{{ model }}
        </option>
      </select>
    </div>

    <div class="field-group">
      <label for="year">Year</label>
      <select id="year" v-model="selectedYear">
        <option value="">Select</option>
        <option
        v-for="year in uniqueYears" :key="year" :value="year">{{ year }}
        </option>
      </select>
    </div>


    <div class="field-group">
      <label for="zip">ZIP</label>
      <input type="text" id="zip" v-model="selectedZIP" list="zip-list" placeholder="Enter">
      <datalist id="zip-list">
        <option v-for="zip in uniqueZIPs" :key="zip" :value="zip">{{ zip }}</option>
      </datalist>
    </div>

    <button @click="doSearch">Search</button>

    <button @click="isAdvanced = !isAdvanced" class="advanced-toggle">
      {{ isAdvanced ? 'Hide' : 'Show' }} Advanced
    </button>

    <div v-if="isAdvanced" class="advanced-fields">
      <div class="field-group">
        <label for="state">State</label>
        <select id="state" v-model="selectedState">
          <option value="">State</option>
          <option v-for="state in uniqueStates" :key="state" :value="state">{{ state }}</option>
        </select>
      </div>

      <div class="field-group">
        <label for="sort">Sort by</label>
        <select id="sort" v-model="sortOrder">
          <option value="newest">Arrival: Newest</option>
          <option value="oldest">Arrival: Oldest</option>
          <option value="year-newest">Year: Newest</option>
          <option value="year-oldest">Year: Oldest</option>
        </select>
      </div>
    </div>
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
      uniqueYears: [],
      uniqueZIPs: [],
      uniqueStates: [],
      selectedMake: '',
      selectedModel: '',
      selectedYear: '',
      selectedZIP: '',
      selectedState: '',
      sortOrder: 'newest',
      isAdvanced: false
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

      const years = data.map(car => car.car_year).filter(Boolean)
      this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

      const models = data.map(car => car.car_model).filter(Boolean)
      this.uniqueModels = [...new Set(models)].sort()

      const zips = data.map(car => car.junkyard_zip).filter(Boolean)
      this.uniqueZIPs = [...new Set(zips)].sort()

      const states = data.map(car => car.junkyard_state).filter(Boolean)
      this.uniqueStates = [...new Set(states)].sort()

    } catch (err) {
      console.error('Error loading makes:', err)
    }
  },
  watch: {
  selectedMake(newMake) {
    if (!newMake) {
      const allModels = this.cars
        .map(car => car.car_model)
        .filter(Boolean)
      this.uniqueModels = [...new Set(allModels)].sort()

      const allYears = this.cars
        .map(car => car.car_year)
        .filter(Boolean)
      this.uniqueYears = [...new Set(allYears)].sort((a, b) => b - a)

      return
    }

    const models = this.cars
      .filter(car => car.car_make === newMake)
      .map(car => car.car_model)
      .filter(Boolean)
    this.uniqueModels = [...new Set(models)].sort()

    const years = this.cars
      .filter(car => car.car_make === newMake)
      .map(car => car.car_year)
      .filter(Boolean)
    this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

    if (this.selectedModel && !this.uniqueModels.includes(this.selectedModel)) {
      this.selectedModel = ''
    }

    if (this.selectedYear && !this.uniqueYears.includes(parseInt(this.selectedYear))) {
      this.selectedYear = ''
    }
  },

  selectedModel(newModel) {
    if (!this.selectedMake) return

    if (!newModel) {
      const years = this.cars
        .filter(car => car.car_make === this.selectedMake)
        .map(car => car.car_year)
        .filter(Boolean)
      this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

      return
    }

    const years = this.cars
      .filter(car => car.car_make === this.selectedMake && car.car_model === newModel)
      .map(car => car.car_year)
      .filter(Boolean)
    this.uniqueYears = [...new Set(years)].sort((a, b) => b - a)

    if (this.selectedYear && !this.uniqueYears.includes(parseInt(this.selectedYear))) {
      this.selectedYear = ''
    }
  }
},

methods: {
  doSearch() {
    this.$emit('search', {
      make: this.selectedMake,
      model: this.selectedModel,
      year: this.selectedYear,
      zip: this.selectedZIP,
      state: this.selectedState,
      sort: this.sortOrder
    })
  }
}
}
</script>

<style scoped>
.search-bar {
  width: 95%; 
  margin: 20px auto;
  padding: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 16px;
  background-color: white;
  box-sizing: border-box;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 40px;
}

.field-group label {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 60px;
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
  width: 150px;
}
.advanced-toggle {
  font-size: 1rem;
  padding: 10px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  background-color: #f8f9fa;
  color: #2c3e50;
  cursor: pointer;
  margin-left: 10px;
}

.advanced-toggle:hover {
  background-color: #e9ecef;
}

.advanced-fields {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
  margin-top: 20px;
  width: 100%;
  justify-content: center;
}
</style>